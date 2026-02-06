from django.contrib import admin
from unfold import admin as unfold

from .models import User, SavedProduct, Basket, Client

# Register your models here.
@admin.register(User)
class UserAdmin(unfold.ModelAdmin):
    list_display = (
        "id", "phone_number", "full_name", "created_at"
    )
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Telegram", {
            "fields": ("tg_id", "tg_username", "tg_full_name",)
        }),
        ("Личная информация", {
            "fields": ("first_name", "last_name",)
        }),
        ("Контакты", {
            "fields": ("phone_number",)
        }),
        ("Системная информация", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
            "description": "Автоматические системные поля (только для чтения)."
        }),
    )

    @unfold.display(description="ФИО")
    def full_name(self, obj):
        if obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.first_name


@admin.register(SavedProduct)
class SavedProductAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
    )
    list_filter = (
        "user",
        "product__category",
        "product__category__category_type",
    )
    search_fields = (
        "user__username",
        "product__title",
    )
    ordering = ("-id",)
    list_display_links = ("id", "product")

    fieldsets = (
        ("Пользователь", {
            "fields": ("user",),
        }),
        ("Товар", {
            "fields": ("product",),
        }),
    )


# =========================
# BASKET ADMIN
# =========================

@admin.register(Basket)
class BasketAdmin(unfold.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "size",
    )
    list_filter = (
        "user",
        "product__category",
        "product__category__category_type",
        "size",
    )
    search_fields = (
        "user__username",
        "product__title",
    )
    ordering = ("-id",)
    list_display_links = ("id", "product")

    fieldsets = (
        ("Пользователь", {
            "fields": ("user",),
        }),
        ("Товар", {
            "fields": ("product",),
        }),
        ("Параметры", {
            "fields": ("size",),
        }),
    )
    
@admin.register(Client)
class ClientAdmin(unfold.ModelAdmin):
    # ===== LIST VIEW =====
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "created_at",
    )
    list_display_links = ("id", "first_name")
    ordering = ("-id",)

    # ===== SEARCH & FILTER =====
    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
    )

    # ===== FORM SETTINGS =====
    fieldsets = (
        ("Основная информация", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
            )
        }),
        ("Системная информация", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # ===== UX IMPROVEMENTS =====
    list_per_page = 25
    save_on_top = True

    def get_queryset(self, request):
        """
        Optimize admin queries (future-proof).
        """
        qs = super().get_queryset(request)
        return qs