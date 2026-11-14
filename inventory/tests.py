
from django.test import TestCase

from catalog.models import (
    Brand,
    Category,
    Product,
    ProductVariant,
)
from .models import Inventory


class InventoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(
            name="Взуття",
            slug="vzuttia",
        )
        brand = Brand.objects.create(
            name="Nike",
            slug="nike",
        )
        product = Product.objects.create(
            name="Кросівки",
            slug="krosivky",
            category=category,
            brand=brand,
            description="Спортивне взуття",
            price="2500.00",
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="NIKE-001",
        )
        cls.inventory = Inventory.objects.create(
            variant=variant,
            quantity=20,
            reserved_quantity=5,
        )

    def test_available_quantity(self):
        self.assertEqual(
            self.inventory.available_quantity,
            15,
        )

    def test_inventory_quantity(self):
        self.assertEqual(
            self.inventory.quantity,
            20,
        )

    def test_reserved_quantity(self):
        self.assertEqual(
            self.inventory.reserved_quantity,
            5,
        )


# Create your tests here.
