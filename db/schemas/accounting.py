from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import event

from db.config import BaseModel


class PaymentsTable(BaseModel):
    __tablename__ = "accounting_payment"

    # OrderTypeChoices -> keep as string
    order_type: Mapped[str] = mapped_column(String(50), nullable=False)

    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("orders_order.id", ondelete="CASCADE"),
        nullable=True,
    )
    sale_id: Mapped[int | None] = mapped_column(
        ForeignKey("sales_sale.id", ondelete="CASCADE"),
        nullable=True,
    )

    # PaymentTypeChoices -> keep as string
    payment_type: Mapped[str] = mapped_column(String(50), nullable=False, default="payme")

    order: Mapped["OrdersTable | None"] = relationship("OrdersTable", back_populates="transactions", lazy="selectin")
    sale: Mapped["SalesTable | None"] = relationship("SalesTable", back_populates="transactions", lazy="selectin")

    def __str__(self) -> str:
        target = self.order or self.sale
        amount = (getattr(self.order, "amount", None) or getattr(self.sale, "amount", None) or 0)
        return f"Оплата №{getattr(self, 'id', '')} — {target} | {amount} so'm | {self.payment_type}"

    def validate(self) -> None:
        if not self.order_id and not self.sale_id:
            raise ValueError("Оплата должна быть связана с заказом или продажей.")
        if self.order_id and self.sale_id:
            raise ValueError("Оплата не может быть связана одновременно с заказом и продажей.")


@event.listens_for(PaymentsTable, "before_insert")
@event.listens_for(PaymentsTable, "before_update")
def _payment_validate(mapper, connection, target: PaymentsTable):
    target.validate()