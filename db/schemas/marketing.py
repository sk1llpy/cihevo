from __future__ import annotations

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from db.config import BaseModel


class PromocodesTable(BaseModel):
    __tablename__ = "marketing_promocode"

    promocode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    discount_uzs: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)

    minimum_price: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)

    expires_at: Mapped[object | None] = mapped_column(DateTime, nullable=True)
    maximum_users: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __str__(self) -> str:
        return self.promocode

    def validate(self) -> None:
        if not self.discount_uzs and not self.discount_percent:
            raise ValueError("Необходимо указать сумму или процент скидки.")
        if self.discount_uzs and self.discount_percent:
            raise ValueError("Можно указать только один тип скидки: сумма или процент.")


class DiscountsTable(BaseModel):
    __tablename__ = "marketing_discount"

    discount_uzs: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)
    discount_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)

    minimum_price: Mapped[float | None] = mapped_column(Numeric(13, 2), nullable=True)

    expires_at: Mapped[object | None] = mapped_column(DateTime, nullable=True)
    maximum_users: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __str__(self) -> str:
        if self.discount_percent:
            return f"{self.discount_percent}%"
        if self.discount_uzs:
            return f"{self.discount_uzs} сум"
        return f"Скидка #{getattr(self, 'id', '')}"

    def validate(self) -> None:
        if not self.discount_uzs and not self.discount_percent:
            raise ValueError("Необходимо указать сумму или процент скидки.")
        if self.discount_uzs and self.discount_percent:
            raise ValueError("Можно указать только один тип скидки.")