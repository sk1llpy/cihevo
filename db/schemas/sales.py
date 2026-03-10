from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.config import BaseModel


class SalesTable(BaseModel):
    __tablename__ = "sales_sale"

    client_id: Mapped[int | None] = mapped_column(
        ForeignKey("users_client.id", ondelete="SET NULL"),
        nullable=True,
    )

    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    promocode_id: Mapped[int | None] = mapped_column(
        ForeignKey("marketing_promocode.id", ondelete="SET NULL"),
        nullable=True,
    )
    discount_id: Mapped[int | None] = mapped_column(
        ForeignKey("marketing_discount.id", ondelete="SET NULL"),
        nullable=True,
    )

    custom_discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    custom_discount_uzs: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)

    client: Mapped["ClientsTable | None"] = relationship("ClientsTable", back_populates="sales", lazy="selectin")
    promocode: Mapped["PromocodesTable | None"] = relationship("PromocodesTable", lazy="selectin")
    discount: Mapped["DiscountsTable | None"] = relationship("DiscountsTable", lazy="selectin")

    products: Mapped[list["SaleProductsTable"]] = relationship(
        "SaleProductsTable",
        back_populates="sale",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    transactions: Mapped[list["PaymentsTable"]] = relationship(
        "PaymentsTable",
        back_populates="sale",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return f"Продажа №{getattr(self, 'id', '')}"

    def calculate_amount(self) -> float:
        total = 0.0
        for item in self.products:
            product = item.product
            if product.in_sale and product.sale_price:
                total += float(product.sale_price)
            else:
                total += float(product.price)

        if self.custom_discount_percent:
            total -= total * float(self.custom_discount_percent) / 100.0

        if self.custom_discount_uzs:
            total -= float(self.custom_discount_uzs)

        return max(total, 0.0)

    def recompute_amount(self) -> None:
        self.amount = self.calculate_amount()


class SaleProductsTable(BaseModel):
    __tablename__ = "sales_saleproduct"
    __table_args__ = (
        UniqueConstraint("sale_id", "product_id", "size", name="uq_sales_saleproduct_sale_product_size"),
    )

    sale_id: Mapped[int] = mapped_column(ForeignKey("sales_sale.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("shop_product.id", ondelete="CASCADE"), nullable=False)

    # SizeChoices -> string
    size: Mapped[str] = mapped_column(String(50), nullable=False)

    sale: Mapped["SalesTable"] = relationship("SalesTable", back_populates="products", lazy="selectin")
    product: Mapped["ProductsTable"] = relationship("ProductsTable", lazy="selectin")

    def __str__(self) -> str:
        return f"{self.product} ({self.size}) — продажа №{self.sale_id}"