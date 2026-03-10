from __future__ import annotations

import random

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import event, select

from db.config import BaseModel


class CategoriesTable(BaseModel):
    __tablename__ = "shop_category"

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ImageField -> store path
    photo: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # CategoryTypeChoices -> string
    category_type: Mapped[str] = mapped_column(String(255), nullable=False, default="default")

    products: Mapped[list["ProductsTable"]] = relationship(
        "ProductsTable",
        back_populates="category",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return self.title or f"Категория #{getattr(self, 'id', '')}"


class BrandsTable(BaseModel):
    __tablename__ = "shop_brand"

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo: Mapped[str | None] = mapped_column(String(512), nullable=True)

    products: Mapped[list["ProductsTable"]] = relationship(
        "ProductsTable",
        back_populates="brand",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"Бренд: {self.title}"


class ProductsTable(BaseModel):
    __tablename__ = "shop_product"

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    brand_id: Mapped[int] = mapped_column(ForeignKey("shop_brand.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("shop_category.id", ondelete="CASCADE"), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ColorTypeChoices -> string
    color: Mapped[str | None] = mapped_column(String(255), nullable=True)

    cost_price: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(13, 2), nullable=False)

    in_sale: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sale_price: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)

    brand: Mapped["BrandsTable"] = relationship("BrandsTable", back_populates="products", lazy="selectin")
    category: Mapped["CategoriesTable"] = relationship("CategoriesTable", back_populates="products", lazy="selectin")

    photos: Mapped[list["ProductPhotosTable"]] = relationship(
        "ProductPhotosTable",
        back_populates="product",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    store_items: Mapped[list["StoreProductsTable"]] = relationship(
        "StoreProductsTable",
        back_populates="product",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return self.title or f"Товар #{getattr(self, 'id', '')}"


class ProductPhotosTable(BaseModel):
    __tablename__ = "shop_productphoto"

    product_id: Mapped[int] = mapped_column(ForeignKey("shop_product.id", ondelete="CASCADE"), nullable=False)

    # ImageField -> store path
    photo: Mapped[str] = mapped_column(String(512), nullable=False)

    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    product: Mapped["ProductsTable"] = relationship("ProductsTable", back_populates="photos", lazy="selectin")

    def __str__(self) -> str:
        return f"Фото для {self.product}"


class StoreProductsTable(BaseModel):
    __tablename__ = "shop_storeproduct"
    __table_args__ = (
        UniqueConstraint("barcode", name="uq_shop_storeproduct_barcode"),
        Index("ix_shop_storeproduct_product_id", "product_id"),
    )

    product_id: Mapped[int] = mapped_column(ForeignKey("shop_product.id", ondelete="CASCADE"), nullable=False)

    # SizeChoices -> string
    size: Mapped[str | None] = mapped_column(String(255), nullable=True)

    barcode: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["ProductsTable"] = relationship("ProductsTable", back_populates="store_items", lazy="selectin")

    def __str__(self) -> str:
        size = self.size or "Без размера"
        return f"{self.product} | {size} | {self.quantity} шт."

    @staticmethod
    def _generate_ean13() -> str:
        base = "".join(str(random.randint(0, 9)) for _ in range(12))
        total = sum(int(d) if i % 2 == 0 else int(d) * 3 for i, d in enumerate(base))
        checksum = (10 - (total % 10)) % 10
        return base + str(checksum)


# ---------- Events (equivalent to Django save logic) ----------

@event.listens_for(StoreProductsTable, "before_insert")
def _storeproduct_autobarcode(mapper, connection, target: StoreProductsTable):
    if target.barcode:
        return

    # Generate until unique
    while True:
        candidate = StoreProductsTable._generate_ean13()
        exists = connection.execute(
            select(StoreProductsTable.id).where(StoreProductsTable.barcode == candidate).limit(1)
        ).first()
        if not exists:
            target.barcode = candidate
            return


@event.listens_for(ProductsTable, "after_insert")
def _product_create_default_store_rows(mapper, connection, target: ProductsTable):
    """
    Django Product.save() created StoreProduct rows based on category_type.
    Here we do the same in DB-level after_insert.
    """
    category_type = connection.execute(
        select(CategoriesTable.category_type).where(CategoriesTable.id == target.category_id).limit(1)
    ).scalar_one_or_none()

    default_sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    shoe_sizes = ["shoes_37", "shoes_38", "shoes_39", "shoes_40", "shoes_41", "shoes_42", "shoes_43", "shoes_44", "shoes_45"]
    jeans_sizes = ["jeans_29", "jeans_30", "jeans_31", "jeans_32", "jeans_33", "jeans_34", "jeans_36", "jeans_38", "jeans_40", "jeans_42"]
    monar_sizes = ["monar_40", "monar_42", "monar_44", "monar_46", "monar_48", "monar_50", "monar_52", "monar_54"]
    suit_sizes = ["suit_44", "suit_46", "suit_48", "suit_50", "suit_52", "suit_54", "suit_56", "suit_58", "suit_60", "suit_62"]

    sizes_map = {
        "default": default_sizes,
        "shoes": shoe_sizes,
        "jeans": jeans_sizes,
        "monar": monar_sizes,
        "suit": suit_sizes,
    }

    for size in sizes_map.get(category_type or "default", default_sizes):
        connection.execute(
            StoreProductsTable.__table__.insert().values(product_id=target.id, size=size, quantity=0)
        )