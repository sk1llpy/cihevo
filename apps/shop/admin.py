from django.contrib import admin
from django.db import models
from unfold import admin as unfold
from apps.general.utils.print_price import generate_labels_batch
from .models import Category, Product, ProductPhoto, StoreProduct, Brand


# =========================
# ADMIN ACTION: Print Labels
# =========================
def format_number(number: int) -> str:
    """
    Format an integer with dots as thousands separators.
    Example: 1000 -> "1.000", 100000 -> "100.000", 1000000 -> "1.000.000"
    """
    return f"{number:,}".replace(",", ".")


def print_labels_action(modeladmin, request, queryset):
    """
    Admin action: Print labels for selected StoreProduct objects.
    Each label will be printed according to the product quantity.
    """
    labels_to_print = []

    for product in queryset:
        for _ in range(product.quantity):
            labels_to_print.append({
                "title": product.product.title,
                "price_original": f"Razmer: {product.size}",
                "barcode": product.barcode,
                "price_sale": f"{format_number(int(product.product.price))} so'm",
            })

    generate_labels_batch(labels_to_print)

    modeladmin.message_user(request, f"Будет напечатано {len(labels_to_print)} этикеток.")


print_labels_action.short_description = "Печать этикетки"


# =========================
# INLINES
# =========================
class ProductPhotoInline(unfold.TabularInline):
    model = ProductPhoto
    extra = 1
    fields = ("photo", "is_main")
    ordering = ("-is_main",)


class StoreProductInline(unfold.TabularInline):
    model = StoreProduct
    extra = 0
    fields = ("size", "quantity")
    readonly_fields = ("size",)
    ordering = ("size",)
    can_delete = False


# =========================
# CATEGORY ADMIN
# =========================
@admin.register(Category)
class CategoryAdmin(unfold.ModelAdmin):
    list_display = ("id", "title", "category_type")
    list_filter = ("category_type",)
    search_fields = ("title",)
    ordering = ("-id",)
    list_display_links = ("id", "title")

    fieldsets = (
        ("Основная информация", {"fields": ("title", "category_type")}),
        ("Описание", {"fields": ("description",)}),
        ("Изображение", {"fields": ("photo",)}),
    )


# =========================
# BRAND ADMIN
# =========================
@admin.register(Brand)
class BrandAdmin(unfold.ModelAdmin):
    list_display = ("title", "logo_preview")
    search_fields = ("title",)
    ordering = ("-id",)
    list_display_links = ("id", "title")
    readonly_fields = ("logo_preview",)

    fieldsets = (("Основная информация", {"fields": ("title", "logo")}),)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="max-height:50px;" />'
        return "-"
    logo_preview.short_description = "Логотип"
    logo_preview.allow_tags = True


# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "brand",
        "price",
        "in_sale",
        "sale_price",
    )
    list_filter = ("category", "category__category_type", "in_sale", "brand")
    search_fields = ("title", "brand__title")
    autocomplete_fields = ("brand",)
    ordering = ("-id",)
    list_editable = ("in_sale",)
    list_display_links = ("id", "title")

    fieldsets = (
        ("Основная информация", {"fields": ("title", "category", "brand")}),
        ("Описание и характеристики", {"fields": ("description", "color")}),
        ("Цены", {"fields": ("price", "in_sale", "sale_price", "cost_price")}),
    )

    inlines = (ProductPhotoInline,)

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj:
            inlines.append(StoreProductInline(self.model, self.admin_site))
        return inlines


# =========================
# STORE PRODUCT ADMIN
# =========================
@admin.register(StoreProduct)
class StoreProductAdmin(unfold.ModelAdmin):
    list_display = ("id", "product", "size", "quantity")
    list_filter = (
        "product",
        "product__category",
        "product__category__category_type",
        "size",
    )
    readonly_fields = ("barcode",)
    search_fields = ("product__title", "barcode")
    ordering = ("product", "size")
    list_editable = ("quantity",)
    list_display_links = ("id", "product")

    fieldsets = (
        ("Основная информация", {"fields": ("product", "size")}),
        ("Склад", {"fields": ("quantity",)}),
        ("Штрих-код", {"fields": ("barcode",)}),
    )

    actions = [print_labels_action]


# =========================
# PRODUCT PHOTO ADMIN
# =========================
@admin.register(ProductPhoto)
class ProductPhotoAdmin(unfold.ModelAdmin):
    list_display = ("id", "product", "is_main")
    list_filter = ("is_main",)
    ordering = ("-is_main", "-id")

    fieldsets = (
        ("Изображение", {"fields": ("product", "photo")}),
        ("Настройки", {"fields": ("is_main",)}),
    )
