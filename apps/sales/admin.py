from django.contrib import admin
from unfold import admin as unfold

from .models import Sale, SaleProduct


# =========================
# INLINE: PRODUCTS IN SALE
# =========================
class SaleProductInline(unfold.TabularInline):
    model = SaleProduct
    extra = 1
    autocomplete_fields = ("product",)
    fields = ("product", "size")
    ordering = ("-id",)


# =========================
# SALE ADMIN
# =========================
@admin.register(Sale)
class SaleAdmin(unfold.ModelAdmin):
    # ===== LIST VIEW =====
    list_display = (
        "id",
        "client",
        "amount",
        "promocode",
        "discount",
        "created_at",
    )
    list_display_links = ("id",)
    ordering = ("-id",)

    # ===== FILTERS & SEARCH =====
    list_filter = (
        "created_at",
        "promocode",
        "discount",
    )
    search_fields = (
        "id",
        "client__first_name",
        "client__last_name",
        "client__phone_number",
    )
    autocomplete_fields = ("client", "promocode", "discount")

    # ===== FORM =====
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "client",
                "amount",
            )
        }),
        ("Скидки", {
            "fields": (
                "promocode",
                "discount",
                "custom_discount_percent",
                "custom_discount_uzs",
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
        "amount",
        "created_at",
        "updated_at",
    )

    inlines = (SaleProductInline,)

    save_on_top = True
    list_per_page = 25


# =========================
# SALE PRODUCT ADMIN
# =========================
@admin.register(SaleProduct)
class SaleProductAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "sale",
        "product",
        "size",
        "created_at",
    )
    list_display_links = ("id", "product")
    ordering = ("-id",)

    list_filter = (
        "size",
        "product",
    )

    search_fields = (
        "sale__id",
        "product__title",
    )

    autocomplete_fields = ("sale", "product")

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "sale",
                "product",
                "size",
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