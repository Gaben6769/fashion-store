from django.db import models


class Inventory(models.Model):
    """Складський залишок конкретного варіанта товару."""

    variant = models.OneToOneField(
        "catalog.ProductVariant",
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name="Варіант товару",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Загальна кількість",
    )
    reserved_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Зарезервована кількість",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення",
    )

    class Meta:
        verbose_name = "Складський залишок"
        verbose_name_plural = "Складські залишки"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    reserved_quantity__lte=models.F("quantity"),
                ),
                name="reserved_not_greater_than_quantity",
            ),
        ]

    def __str__(self):
        return f"{self.variant} — {self.available_quantity} шт."

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity