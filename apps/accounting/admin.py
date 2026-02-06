from django.contrib import admin
from unfold import admin as unfold

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(unfold.ModelAdmin):
    # ===== LIST VIEW =====
    list_display = (
        "id",
        "order_type",
        "order",
        "sale",
        "payment_type",
        "created_at",
    )
    list_display_links = ("id",)
    ordering = ("-id",)

    # ===== FILTERS =====
    list_filter = (
        "order_type",
        "payment_type",
        "created_at",
    )

    # ===== SEARCH =====
    search_fields = (
        "id",
        "order__id",
        "sale__id",
    )

    # ===== FORM =====
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "order_type",
                "payment_type",
            )
        }),
        ("Связь", {
            "fields": (
                "order",
                "sale",
            )
        }),
        ("Системная информация", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    autocomplete_fields = ("order", "sale")

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    save_on_top = True
    list_per_page = 25