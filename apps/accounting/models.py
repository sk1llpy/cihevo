from django.db import models
from django.core.exceptions import ValidationError

from apps.general.models import BaseModel
from apps.general.choices import (
    PaymentTypeChoices,
    OrderStatusTypeChoices,
    OrderTypeChoices,
)
from apps.orders.models import Order
from apps.sales.models import Sale


class Payment(BaseModel):
    order_type = models.CharField(
        max_length=50,
        choices=OrderTypeChoices.choices,
        verbose_name="Тип заказа",
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Заказ",
        related_name="transactions",
    )

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Продажа",
        related_name="transactions",
    )

    payment_type = models.CharField(
        max_length=50,
        choices=PaymentTypeChoices.choices,
        default=PaymentTypeChoices.PAYME,
        verbose_name="Тип оплаты",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Платежи"
        ordering = ("-id",)

    def __str__(self):
        target = self.order or self.sale
        amount = (
            getattr(self.order, "amount", None)
            or getattr(self.sale, "amount", None)
            or 0
        )
        return f"Оплата №{self.id} — {target} | {amount} so'm | {self.payment_type}"

    # =========================
    # VALIDATION
    # =========================
    def clean(self):
        if not self.order and not self.sale:
            raise ValidationError("Оплата должна быть связана с заказом или продажей.")
        if self.order and self.sale:
            raise ValidationError("Оплата не может быть связана одновременно с заказом и продажей.")

    # =========================
    # SAVE LOGIC
    # =========================
    def save(self, *args, **kwargs):
        self.full_clean()

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.order:
            if self.order.status == OrderStatusTypeChoices.WAITING_PAYMENT:
                self.order.status = OrderStatusTypeChoices.PENDING
                self.order.save(update_fields=["status"])