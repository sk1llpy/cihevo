from django.db import models
from django.core.exceptions import ValidationError
from apps.general.models import BaseModel


class Promocode(BaseModel):
    promocode = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Промокод",
    )

    discount_uzs = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Скидка (сум)",
    )

    discount_percent = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Скидка (%)",
    )

    minimum_price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Минимальная сумма",
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата окончания",
    )

    maximum_users = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Максимальное количество использований",
    )

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ("-id",)

    def __str__(self):
        return self.promocode

    def clean(self):
        if not self.discount_uzs and not self.discount_percent:
            raise ValidationError("Необходимо указать сумму или процент скидки.")
        if self.discount_uzs and self.discount_percent:
            raise ValidationError("Можно указать только один тип скидки: сумма или процент.")


class Discount(BaseModel):
    discount_uzs = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Скидка (сум)",
    )

    discount_percent = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Скидка (%)",
    )

    minimum_price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Минимальная сумма",
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата окончания",
    )

    maximum_users = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Максимальное количество использований",
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        ordering = ("-id",)

    def __str__(self):
        if self.discount_percent:
            return f"{self.discount_percent}%"
        if self.discount_uzs:
            return f"{self.discount_uzs} сум"
        return f"Скидка #{self.id}"

    def clean(self):
        if not self.discount_uzs and not self.discount_percent:
            raise ValidationError("Необходимо указать сумму или процент скидки.")
        if self.discount_uzs and self.discount_percent:
            raise ValidationError("Можно указать только один тип скидки.")