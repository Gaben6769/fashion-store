from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Brand, Category, Product


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Чоловічий одяг",
            slug="cholovichyi-odiah",
        )
        cls.brand = Brand.objects.create(
            name="Nike",
            slug="nike",
        )
        cls.product = Product.objects.create(
            name="Базова футболка",
            slug="bazova-futbolka",
            category=cls.category,
            brand=cls.brand,
            description="Біла футболка",
            price=Decimal("1499.00"),
            old_price=Decimal("1799.00"),
            is_active=True,
        )

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)

    def test_product_has_discount(self):
        self.assertTrue(self.product.has_discount)

    def test_discount_percent(self):
        self.assertEqual(self.product.discount_percent, 17)

    def test_product_without_discount(self):
        self.product.old_price = None
        self.assertFalse(self.product.has_discount)
        self.assertEqual(self.product.discount_percent, 0)

    def test_catalog_page(self):
        response = self.client.get(
            reverse("catalog:product_list")
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Базова футболка")

    def test_search_product(self):
        response = self.client.get(
            reverse("catalog:product_list"),
            {"q": "футболка"},
        )
        self.assertEqual(
            response.context["page_obj"].paginator.count,
            1,
        )

    def test_search_no_results(self):
        response = self.client.get(
            reverse("catalog:product_list"),
            {"q": "ноутбук"},
        )
        self.assertEqual(
            response.context["page_obj"].paginator.count,
            0,
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("catalog:product_list"),
            {"category": self.category.slug},
        )
        self.assertEqual(
            response.context["page_obj"].paginator.count,
            1,
        )

    def test_product_detail(self):
        response = self.client.get(
            self.product.get_absolute_url()
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Базова футболка")


# Create your tests here.
