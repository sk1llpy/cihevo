from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import BaseModel


class UsersTable(BaseModel):
    __tablename__ = "users_user"

    tg_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    tg_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tg_full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=False)

    saved_products: Mapped[list["SavedProductsTable"]] = relationship(
        "SavedProductsTable",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    basket: Mapped[list["BasketTable"]] = relationship(
        "BasketTable",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    orders: Mapped[list["OrdersTable"]] = relationship(
        "OrdersTable",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        if self.last_name:
            return f"{self.first_name or ''} {self.last_name} ({self.phone_number})".strip()
        return f"{self.first_name or ''} ({self.phone_number})".strip()


class SavedProductsTable(BaseModel):
    __tablename__ = "users_savedproduct"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_users_savedproduct_user_product"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_user.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("shop_product.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["UsersTable"] = relationship("UsersTable", back_populates="saved_products", lazy="selectin")
    product: Mapped["ProductsTable"] = relationship("ProductsTable", lazy="selectin")

    def __str__(self) -> str:
        return f"{self.user} — {self.product}"


class BasketTable(BaseModel):
    __tablename__ = "users_basket"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_user.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("shop_product.id", ondelete="CASCADE"),
        nullable=False,
    )

    # SizeChoices -> keep as string
    size: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped["UsersTable"] = relationship("UsersTable", back_populates="basket", lazy="selectin")
    product: Mapped["ProductsTable"] = relationship("ProductsTable", lazy="selectin")

    def __str__(self) -> str:
        size = self.size or "Без размера"
        return f"{self.user} — {self.product} ({size})"


class ClientsTable(BaseModel):
    __tablename__ = "users_client"

    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(255), nullable=True)

    sales: Mapped[list["SalesTable"]] = relationship(
        "SalesTable",
        back_populates="client",
        lazy="selectin",
    )

    def __str__(self) -> str:
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name or (self.phone_number or f"Клиент #{getattr(self, 'id', '')}")