from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Назва",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="URL-ідентифікатор",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Опис",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Назва",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="URL-ідентифікатор",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Опис",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Назва",
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        verbose_name="URL-ідентифікатор",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категорія",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Бренд",
    )
    description = models.TextField(
        verbose_name="Опис",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Ціна",
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Стара ціна",
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Зображення",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )
    is_new = models.BooleanField(
        default=True,
        verbose_name="Новинка",
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Рекомендований",
    )
    popularity_score = models.PositiveIntegerField(
        default=0,
        verbose_name="Популярність",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "catalog:product_detail",
            kwargs={"slug": self.slug},
        )

    @property
    def has_discount(self):
        return bool(self.old_price and self.old_price > self.price)

    @property
    def discount_percent(self):
        if not self.has_discount:
            return 0

        discount = (self.old_price - self.price) / self.old_price * 100
        return round(discount)


class Size(models.Model):
    """Розмір товару."""

    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Назва",
    )
    size_type = models.CharField(
        max_length=30,
        choices=[
            ("clothing", "Одяг"),
            ("shoes", "Взуття"),
            ("universal", "Універсальний"),
        ],
        default="clothing",
        verbose_name="Тип розміру",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортування",
    )

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Розмір"
        verbose_name_plural = "Розміри"

    def __str__(self):
        return str(self.name)


class Color(models.Model):
    """Колір товару."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Назва",
    )
    hex_code = models.CharField(
        max_length=7,
        default="#000000",
        verbose_name="HEX-код",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Колір"
        verbose_name_plural = "Кольори"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Конкретний варіант товару за розміром і кольором."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Товар",
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.PROTECT,
        related_name="product_variants",
        blank=True,
        null=True,
        verbose_name="Розмір",
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        related_name="product_variants",
        blank=True,
        null=True,
        verbose_name="Колір",
    )
    sku = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Артикул",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )

    class Meta:
        verbose_name = "Варіант товару"
        verbose_name_plural = "Варіанти товару"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "size", "color"],
                name="unique_product_size_color",
            ),
        ]

    def __str__(self):
        attributes = [
            value
            for value in [
                self.size.name if self.size else None,
                self.color.name if self.color else None,
            ]
            if value
        ]

        suffix = " / ".join(attributes)
        return f"{self.product.name} ({suffix})" if suffix else self.product.name