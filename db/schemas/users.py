from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from db.config import BaseModel

class UsersTable(BaseModel):
    __tablename__ = 'users_user'

    tg_id: Mapped[str] = mapped_column()
    tg_username: Mapped[str] = mapped_column()
    tg_full_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    
    saved_products: Mapped[list["SavedProductsTable"]] = relationship(lazy="selectin", back_populates="user")
    basket: Mapped[list["BasketTable"]] = relationship(lazy="selectin", back_populates="user")


class SavedProductsTable(BaseModel):
    __tablename__ = 'users_savedproduct'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('shop_product.id'))
    
    user: Mapped["UsersTable"] = relationship(lazy="selectin", back_populates="saved_products")
    product: Mapped["ProductsTable"] = relationship(lazy="selectin", back_populates="saved_products")


class BasketTable(BaseModel):
    __tablename__ = 'users_basket'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('shop_product.id'))
    size: Mapped[str] = mapped_column()
    
    user: Mapped["UsersTable"] = relationship(lazy="selectin", back_populates="basket")
    product: Mapped["ProductsTable"] = relationship(lazy="selectin", back_populates="basket")


class ClientsTable(BaseModel):
    __tablename__ = 'users_client'
    
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
