from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import BaseModel


class OrdersTable(BaseModel):
    __tablename__ = "orders_order"

    user_id: Mapped[int] = mapped_column(ForeignKey("users_user.id", ondelete="CASCADE"), nullable=False)

    phone_number: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(String(320), nullable=True)

    # OrderStatusTypeChoices -> keep as string
    status: Mapped[str] = mapped_column(String(255), nullable=False, default="waiting_payment")

    amount: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)

    promocode_id: Mapped[int | None] = mapped_column(
        ForeignKey("marketing_promocode.id", ondelete="SET NULL"),
        nullable=True,
    )
    discount_id: Mapped[int | None] = mapped_column(
        ForeignKey("marketing_discount.id", ondelete="SET NULL"),
        nullable=True,
    )

    user: Mapped["UsersTable"] = relationship("UsersTable", back_populates="orders", lazy="selectin")
    promocode: Mapped["PromocodesTable | None"] = relationship("PromocodesTable", lazy="selectin")
    discount: Mapped["DiscountsTable | None"] = relationship("DiscountsTable", lazy="selectin")

    products: Mapped[list["OrderProductsTable"]] = relationship(
        "OrderProductsTable",
        back_populates="order",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    transactions: Mapped[list["PaymentsTable"]] = relationship(
        "PaymentsTable",
        back_populates="order",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"Заказ №{getattr(self, 'id', '')} — {self.user}"

    def calculate_amount(self) -> float:
        total = 0.0
        for item in self.products:
            p = item.product
            if p.in_sale and p.sale_price:
                total += float(p.sale_price)
            else:
                total += float(p.price)
        return total

    def recompute_amount(self) -> None:
        self.amount = self.calculate_amount()


class OrderProductsTable(BaseModel):
    __tablename__ = "orders_orderproduct"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", "size", name="uq_orders_orderproduct_order_product_size"),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey("orders_order.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("shop_product.id", ondelete="CASCADE"), nullable=False)

    # SizeChoices -> string
    size: Mapped[str] = mapped_column(String(255), nullable=False)

    order: Mapped["OrdersTable"] = relationship("OrdersTable", back_populates="products", lazy="selectin")
    product: Mapped["ProductsTable"] = relationship("ProductsTable", lazy="selectin")

    def __str__(self) -> str:
        return f"{self.product} ({self.size}) — заказ №{self.order_id}"