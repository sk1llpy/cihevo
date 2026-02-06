from API.config import Versions, RouterSettings
from API.v1.auth.router import router as auth_router
from API.v1.users.router import router as users_router
from API.v1.products.router import router as products_router
from API.v1.cart.router import router as cart_router
from API.v1.saved.router import router as saved_router

def load_routers() -> list[RouterSettings]:
    return (
        RouterSettings(auth_router, Versions.v1, ["auth"]),
        RouterSettings(users_router, Versions.v1, ["users"]),
        RouterSettings(products_router, Versions.v1, ["products"]),
        RouterSettings(cart_router, Versions.v1, ["cart"]),
        RouterSettings(saved_router, Versions.v1, ["saved_products"]),
    )
