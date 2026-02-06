from django.db import models
from django.core.validators import RegexValidator

from apps.general.models import BaseModel
from apps.general.utils import uploaders
from apps.general.choices import SizeChoices, CategoryTypeChoices, ColorTypeChoices


class Category(BaseModel):
    title = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Название"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    photo = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        verbose_name="Фото"
    )
    category_type = models.CharField(
        max_length=255,
        choices=CategoryTypeChoices.choices, 
        default=CategoryTypeChoices.DEFAULT,
        verbose_name="Тип категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("-id",)

    def __str__(self):
        return self.title or f"Категория #{self.id}"


class Brand(BaseModel):
    title = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Название"
    )
    logo = models.ImageField(
        upload_to='brands/',
        null=True,
        blank=True,
        verbose_name="Логотип"
    )
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренд"

    def __str__(self):
        return f"Бренд: {self.title}"


class Product(BaseModel):
    title = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Название"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name="Бренд"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    color = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=ColorTypeChoices.choices,
        verbose_name="Цвет"
    )
    cost_price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="Себестоимость (таннарх)",
        null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        verbose_name="Цена"
    )
    in_sale = models.BooleanField(
        default=False,
        verbose_name="В распродаже"
    )
    sale_price = models.DecimalField(
        max_digits=13,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена со скидкой"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-id",)

    def __str__(self):
        return self.title or f"Товар #{self.id}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            default_sizes = ["XS", "S", "M", "L", "XL", "XXL"]
            shoe_sizes = [
                "shoes_37", "shoes_38", "shoes_39", "shoes_40", 
                "shoes_41", "shoes_42", "shoes_43", "shoes_44", "shoes_45"
            ]
            jeans_sizes = [
                "jeans_29", "jeans_30", "jeans_31", "jeans_32", 
                "jeans_33", "jeans_34", "jeans_36", "jeans_38", 
                "jeans_40", "jeans_42"
            ]
            monar_sizes = [
                "monar_40", "monar_42", "monar_44", "monar_46",
                "monar_48", "monar_50", "monar_52", "monar_54"
            ]
            suit_sizes = [
                "suit_44", "suit_46", "suit_48", "suit_50", 
                "suit_52", "suit_54", "suit_56", "suit_58", 
                "suit_60", "suit_62"
            ]
            
            sizes = {
                CategoryTypeChoices.DEFAULT: default_sizes,
                CategoryTypeChoices.SHOES: shoe_sizes,
                CategoryTypeChoices.JEANS: jeans_sizes,
                CategoryTypeChoices.MONAR: monar_sizes,
                CategoryTypeChoices.SUIT: suit_sizes
            }
            
            for size in sizes[self.category.category_type]:
                obj = StoreProduct.objects.create(
                    product = self,
                    size = size
                )
                obj.save()


class ProductPhoto(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    photo = models.ImageField(
        upload_to=uploaders.product_photo_uploader,
        verbose_name="Фото"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Основное фото"
    )

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"
        ordering = ("-is_main", "-id")

    def __str__(self):
        return f"Фото для {self.product}"


class StoreProduct(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    size = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=SizeChoices.choices,
        verbose_name="Размер"
    )
    barcode = models.CharField(
        max_length=64, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="Штрих-код"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товары на складе"
        ordering = ("-id",)

    def __str__(self):
        size = self.size if self.size else "Без размера"
        return f"{self.product} | {size} | {self.quantity} шт."

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = self._generate_unique_barcode()
        super().save(*args, **kwargs)

    def _generate_unique_barcode(self):
        """
        Generate a unique 13-digit EAN13 barcode for this model.
        """
        from django.db import transaction, IntegrityError

        while True:
            barcode = self._generate_ean13()
            # Wrap in atomic transaction to avoid race conditions
            try:
                with transaction.atomic():
                    if not StoreProduct.objects.filter(barcode=barcode).exists():
                        return barcode
            except IntegrityError:
                # Another process may have inserted the same barcode; retry
                continue

    @staticmethod
    def _generate_ean13():
        import random
        base = ''.join(str(random.randint(0, 9)) for _ in range(12))
        total = sum(int(d) if i % 2 == 0 else int(d) * 3 for i, d in enumerate(base))
        checksum = (10 - (total % 10)) % 10
        return base + str(checksum)
