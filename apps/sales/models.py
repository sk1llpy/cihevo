from django.db import models
from apps.general.models import BaseModel
from apps.users.models import Client
from apps.marketing.models import Promocode, Discount
from apps.shop.models import Product
from apps.general.choices import SizeChoices


class Sale(BaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Клиент",
        related_name="sales",
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Итоговая сумма",
        default=0,
    )

    promocode = models.ForeignKey(
        Promocode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Промокод",
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка",
    )

    custom_discount_percent = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Индивидуальная скидка (%)",
    )

    custom_discount_uzs = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Индивидуальная скидка (сум)",
    )

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"
        ordering = ("-id",)

    def __str__(self):
        return f"Продажа №{self.id}"

    # =========================
    # CALCULATE TOTAL AMOUNT
    # =========================
    def calculate_amount(self):
        total = 0

        for item in self.products.select_related("product"):
            product = item.product
            if product.in_sale and product.sale_price:
                total += product.sale_price
            else:
                total += product.price

        # Custom discounts
        if self.custom_discount_percent:
            total -= total * self.custom_discount_percent / 100

        if self.custom_discount_uzs:
            total -= self.custom_discount_uzs

        return max(total, 0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.amount = self.calculate_amount()
        super().save(update_fields=["amount"])

class SaleProduct(BaseModel):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        verbose_name="Продажа",
        related_name="products",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )

    size = models.CharField(
        max_length=50,
        choices=SizeChoices.choices,
        verbose_name="Размер",
    )

    class Meta:
        verbose_name = "Товар в продаже"
        verbose_name_plural = "Товары в продаже"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=["sale", "product", "size"],
                name="unique_sale_product_size",
            )
        ]

    def __str__(self):
        return f"{self.product} ({self.size}) — продажа №{self.sale.id}"