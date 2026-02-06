from sqlalchemy import select, and_, or_
from sqlalchemy.orm import joinedload, selectinload

from db.postgres.repositories import AsyncRepository
from db.postgres.repositories.users import (
    AsyncUserRepository,
    AsyncBasketRepository,
    AsyncSavedProductsRepository,
)
from db.schemas import (
    ProductsTable,
    BrandsTable,
    CategoriesTable,
    BasketTable,
    ProductPhotosTable,
    SavedProductsTable,
    StoreProductsTable,
)


class AsyncProductRepository(AsyncRepository):
    table = ProductsTable

    async def get_products(self) -> list[dict]:
        query = (
            select(ProductsTable)
            .options(
                joinedload(ProductsTable.brand),
                joinedload(ProductsTable.category),
                selectinload(ProductsTable.product_photos),
            )
        )

        result = await self.execute(query=query)
        products = result.scalars().unique().all()

        return [self._serialize_product(product) for product in products]

    async def get_product(self, id: int) -> dict:
        query = (
            select(ProductsTable)
            .where(ProductsTable.id == id)
            .options(
                joinedload(ProductsTable.brand),
                joinedload(ProductsTable.category),
                selectinload(ProductsTable.product_photos),
            )
        )

        result = await self.execute(query=query)
        product = result.scalar_one_or_none()

        if not product:
            return None

        sizes_query = select(StoreProductsTable).where(
            StoreProductsTable.product_id == product.id
        )
        sizes_result = (await self.execute(sizes_query)).scalars().all()

        sizes = [
            {
                "title": obj.size,
                "quantity": obj.quantity,
            }
            for obj in sizes_result
        ]

        return self._serialize_product(product, sizes)

    @staticmethod
    def _serialize_product(product: ProductsTable, sizes: list | None = None) -> dict:
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,

            "brand": {
                "id": product.brand.id,
                "title": product.brand.title,
            } if product.brand else None,

            "category": {
                "id": product.category.id,
                "title": product.category.title,
                "category_type": product.category.category_type,
            } if product.category else None,

            "color": product.color,
            "cost_price": product.cost_price,
            "price": product.price,
            "in_sale": product.in_sale,
            "sale_price": product.sale_price,

            "photos": [
                f"http://localhost:8000/media/{photo.photo}"
                for photo in sorted(
                    product.product_photos,
                    key=lambda p: p.is_main,
                    reverse=True,
                )
            ],

            "sizes": sizes or [],
        }

    async def add_to_cart(self, product_id: int, user_id: int, size=None) -> dict:
        is_exist = await AsyncStoreProductRepository(
            self.session
        ).get_quantity_product(product_id=product_id, size=size)

        if is_exist or is_exist.quantity > 0:
            return await AsyncBasketRepository(self.session).add_product(
                user_id=user_id,
                product_id=product_id,
                size=size
            )
        return {"error": "No product left"}


    async def add_to_saved(self, product_id: int, user_id: int) -> dict:
        user = await AsyncUserRepository(self.session).get(conditions={"id": user_id})
        product = await self.get(conditions={"id": product_id})

        return await AsyncSavedProductsRepository(self.session).add_product(
            user=user, product=product
        )

    async def cart(self, user_id: int) -> dict:
        query = select(BasketTable).where(BasketTable.user_id == user_id)
        result = (await self.execute(query=query)).scalars().all()

        total_price = 0
        total_price_without_sale = 0

        products_map = {}

        for obj in result:
            key = (obj.product.id, obj.size)

            price = (
                obj.product.sale_price
                if obj.product.in_sale and obj.product.sale_price
                else obj.product.price
            )

            total_price += price
            total_price_without_sale += obj.product.price

            if key in products_map:
                products_map[key]["quantity"] += 1
            else:
                products_map[key] = {
                    "id": obj.product.id,
                    "size": obj.size,
                    "quantity": 1,
                    "product": self._serialize_product(obj.product),
                }

        return {
            "total": total_price,
            "total_without_sale": total_price_without_sale,
            "products": list(products_map.values())
        }

    async def filter_products(self, filters: dict) -> list[dict]:
        """
        filters example:
        {
            "size": ["S", "M"],
            "categories": [1,2],
            "colors": ["red", "blue"],
            "in_stock": True,
            "out_of_stock": False,
            "min_price": 0,
            "max_price": 10000000
        }
        """
        query = select(ProductsTable).options(
            joinedload(ProductsTable.brand),
            joinedload(ProductsTable.category),
            selectinload(ProductsTable.product_photos),
        )

        conditions = []

        # Categories (integer)
        if filters.get("categories"):
            categories = []
            for c in filters["categories"]:
                try:
                    categories.append(int(c))
                except (ValueError, TypeError):
                    continue
            if categories:
                conditions.append(ProductsTable.category_id.in_(categories))

        # Colors (string)
        if filters.get("colors"):
            colors = [str(c) for c in filters["colors"]]
            conditions.append(ProductsTable.color.in_(colors))

        # Price
        min_price = filters.get("min_price") or 0
        max_price = filters.get("max_price") or 10_000_000
        conditions.append(
            or_(
                and_(ProductsTable.in_sale == True, ProductsTable.sale_price >= min_price, ProductsTable.sale_price <= max_price),
                and_(ProductsTable.in_sale == False, ProductsTable.price >= min_price, ProductsTable.price <= max_price),
            )
        )

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.execute(query=query)
        products = result.scalars().unique().all()

        filtered_products = []
        in_stock = filters.get("in_stock", False)
        out_of_stock = filters.get("out_of_stock", False)

        for product in products:
            store_query = select(StoreProductsTable).where(StoreProductsTable.product_id == product.id)
            
            # Sizes filter
            if filters.get("size"):
                store_query = store_query.where(StoreProductsTable.size.in_(filters["size"]))

            store_products = (await self.execute(store_query)).scalars().all()
            total_quantity = sum([sp.quantity for sp in store_products])

            # Stock logic:
            # If both in_stock and out_of_stock are True, show all products
            if not (in_stock and out_of_stock):
                if in_stock and total_quantity <= 0:
                    continue
                if out_of_stock and total_quantity > 0:
                    continue

            filtered_products.append(product)

        return [self._serialize_product(p) for p in filtered_products]

    async def saved_products(self, user_id: int) -> dict:
        query = select(SavedProductsTable).where(
            SavedProductsTable.user_id == user_id
        )
        result = (await self.execute(query=query)).scalars().all()

        return [self._serialize_product(obj.product) for obj in result]

    async def remove_saved_product(self, user_id: int, product_id: int) -> dict:
        query = select(ProductsTable).where(ProductsTable.id == product_id)
        obj = (await self.execute(query=query)).scalar_one_or_none()
        if not obj:
            return False

        query_saved = select(SavedProductsTable).where(
            SavedProductsTable.user_id == user_id,
            SavedProductsTable.product_id == obj.id,
        )
        saved_product = (await self.execute(query_saved)).scalar_one_or_none()
        if not saved_product:
            return False

        await self.session.delete(saved_product)
        await self.session.commit()
        return True

    async def remove_cart(self, user_id: int, cart_id: int) -> bool:
        query = select(BasketTable).where(
            BasketTable.user_id == user_id,
            BasketTable.id == cart_id,
        )

        obj = (await self.execute(query)).scalar_one_or_none()
        if not obj:
            return False

        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def get_categories(self):
        query = select(
            CategoriesTable.id,
            CategoriesTable.title,
            CategoriesTable.category_type,
            CategoriesTable.description,
            CategoriesTable.photo,
        )

        return (await self.execute(query)).mappings().all()


class AsyncStoreProductRepository(AsyncRepository):
    table = StoreProductsTable

    async def get_quantity_product(self, product_id, size=None):
        query = select(StoreProductsTable).where(
            StoreProductsTable.product_id == product_id,
            StoreProductsTable.size == size,
        )

        return (await self.execute(query)).scalar_one_or_none()


def get_async_product_repo() -> AsyncProductRepository:
    return AsyncProductRepository()