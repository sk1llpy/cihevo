from django.db import models
from apps.general.models import BaseModel
from apps.shop.models import Product
from apps.general.choices import SizeChoices


class User(BaseModel):
    tg_id = models.CharField(unique=True, verbose_name="Telegram ID")
    tg_username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя пользователя в Telegram")
    tg_full_name = models.CharField(max_length=255, verbose_name="Полное имя в Telegram", null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия", null=True, blank=True)
    phone_number = models.CharField(max_length=255, verbose_name="Номер телефона")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name} ({self.phone_number})"
        return f"{self.first_name} ({self.phone_number})"


class SavedProduct(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )

    class Meta:
        verbose_name = "Сохранённый товар"
        verbose_name_plural = "Сохранённые товары"
        ordering = ("-id",)
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} — {self.product}"


class Basket(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    size = models.CharField(
        max_length=255,
        null=True,
        choices=SizeChoices.choices,
        verbose_name="Размер"
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        ordering = ("-id",)

    def __str__(self):
        size = self.size if self.size else "Без размера"
        return f"{self.user} — {self.product} ({size})"
    

class Client(BaseModel):
    first_name = models.CharField(
        max_length=255,
        verbose_name="Имя",
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=255,
        verbose_name="Номер телефона",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("-id",)

    def __str__(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name or self.phone_number or f"Клиент #{self.id}"