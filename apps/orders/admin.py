from django.contrib import admin
from unfold import admin as unfold
from .models import Order, OrderProduct


# =========================
# INLINES
# =========================

class OrderProductInline(unfold.TabularInline):
    model = OrderProduct
    extra = 0
    fields = ("product", "size")
    autocomplete_fields = ("product",)


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order)
class OrderAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "status",
    )
    list_filter = (
        "status",
        "user",
    )
    search_fields = (
        "user__username",
        "user__email",
        "phone_number",
    )
    ordering = ("-id",)
    list_display_links = ("id",)

    fieldsets = (
        ("Заказ", {
            "fields": ("user", "status"),
        }),
        ("Контактная информация", {
            "fields": ("phone_number", "address"),
        }),
    )

    inlines = (OrderProductInline,)


# =========================
# ORDER PRODUCT ADMIN
# =========================

@admin.register(OrderProduct)
class OrderProductAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "size",
    )
    list_filter = (
        "size",
        "product__category",
        "product__category__category_type",
    )
    search_fields = (
        "order__id",
        "product__title",
    )
    ordering = ("-id",)
    list_display_links = ("id", "product")

    fieldsets = (
        ("Заказ", {
            "fields": ("order",),
        }),
        ("Товар", {
            "fields": ("product", "size"),
        }),
    )
    
