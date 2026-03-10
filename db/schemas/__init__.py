# db/schemas/__init__.py

# users
from .users import (
    UsersTable,
    SavedProductsTable,
    BasketTable,
    ClientsTable,
)

# shop
from .shop import (
    CategoriesTable,
    BrandsTable,
    ProductsTable,
    ProductPhotosTable,
    StoreProductsTable,
)

# marketing
from .marketing import (
    PromocodesTable,
    DiscountsTable,
)

# sales
from .sales import (
    SalesTable,
    SaleProductsTable,
)

# orders
from .orders import (
    OrdersTable,
    OrderProductsTable,
)

# accounting
from .accounting import (
    PaymentsTable,
)

__all__ = [
    # users
    "UsersTable",
    "SavedProductsTable",
    "BasketsTable",
    "ClientsTable",
    # shop
    "CategoriesTable",
    "BrandsTable",
    "ProductsTable",
    "ProductPhotosTable",
    "StoreProductsTable",
    # marketing
    "PromocodesTable",
    "DiscountsTable",
    # sales
    "SalesTable",
    "SaleProductsTable",
    # orders
    "OrdersTable",
    "OrderProductsTable",
    # accounting
    "PaymentsTable",
]