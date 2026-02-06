from django.contrib import admin
from unfold import admin as unfold

from .models import Promocode, Discount


# =========================
# PROMOCODE ADMIN
# =========================
@admin.register(Promocode)
class PromocodeAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "promocode",
        "discount_percent",
        "discount_uzs",
        "minimum_price",
        "expires_at",
        "maximum_users",
        "created_at",
    )
    list_display_links = ("id", "promocode")
    ordering = ("-id",)

    list_filter = (
        "expires_at",
        "created_at",
    )

    search_fields = (
        "promocode",
    )

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "promocode",
            )
        }),
        ("Скидка", {
            "fields": (
                "discount_percent",
                "discount_uzs",
                "minimum_price",
            )
        }),
        ("Ограничения", {
            "fields": (
                "maximum_users",
                "expires_at",
            )
        }),
        ("Системная информация", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True
    list_per_page = 25


# =========================
# DISCOUNT ADMIN
# =========================
@admin.register(Discount)
class DiscountAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "discount_percent",
        "discount_uzs",
        "minimum_price",
        "expires_at",
        "maximum_users",
        "created_at",
    )
    list_display_links = ("id",)
    ordering = ("-id",)

    search_fields = ("id",)
    list_filter = (
        "expires_at",
        "created_at",
    )

    fieldsets = (
        ("Скидка", {
            "fields": (
                "discount_percent",
                "discount_uzs",
                "minimum_price",
            )
        }),
        ("Ограничения", {
            "fields": (
                "maximum_users",
                "expires_at",
            )
        }),
        ("Системная информация", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True
    list_per_page = 25 