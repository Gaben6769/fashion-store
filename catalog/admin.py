from django.contrib import admin

from .models import (
    Brand,
    Category,
    Color,
    Product,
    ProductVariant,
    Size,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "price",
        "is_active",
        "is_new",
        "is_featured",
    )
    list_filter = (
        "is_active",
        "is_new",
        "is_featured",
        "category",
        "brand",
    )
    search_fields = (
        "name",
        "description",
        "brand__name",
        "category__name",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "size_type", "sort_order")
    list_filter = ("size_type",)
    search_fields = ("name",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "size",
        "color",
        "sku",
        "is_active",
    )
    list_filter = ("is_active", "size", "color")
    search_fields = (
        "sku",
        "product__name",
    )