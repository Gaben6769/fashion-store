from django.contrib import admin

from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "variant",
        "quantity",
        "reserved_quantity",
        "available_quantity_display",
        "updated_at",
    )
    search_fields = (
        "variant__sku",
        "variant__product__name",
    )

    @admin.display(description="Доступно")
    def available_quantity_display(self, obj):
        return obj.available_quantity