from django.db import models
from apps.users.models import User
from apps.shop.models import Product
from apps.marketing.models import Promocode, Discount
from apps.general.models import BaseModel
from apps.general.choices import SizeChoices, OrderStatusTypeChoices


class Order(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    phone_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Номер телефона"
    )
    address = models.CharField(
        max_length=320,
        null=True,
        verbose_name="Адрес доставки"
    )
    status = models.CharField(
        max_length=255,
        choices=OrderStatusTypeChoices.choices,
        default=OrderStatusTypeChoices.WAITING_PAYMENT,
        verbose_name="Статус заказа"
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Сумма",
        null=True,
        blank=True
    )
    promocode = models.ForeignKey(
        Promocode, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    discount = models.ForeignKey(
        Discount, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-id",)

    def __str__(self):
        return f"Заказ №{self.id} — {self.user}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.amount = 0
            products = OrderProduct.objects.filter(order=self)
            
            for product in products:
                if product.product.in_sale and product.product.sale_price:
                    self.amount += product.product.sale_price
                self.amount += product.product.price
        
        return super().save(*args, **kwargs)


class OrderProduct(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    size = models.CharField(
        max_length=255,
        choices=SizeChoices.choices,
        verbose_name="Размер"
    )

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
        ordering = ("-id",)
        unique_together = ("order", "product", "size")

    def __str__(self):
        return f"{self.product} ({self.size}) — заказ №{self.order.id}"
    
