import uuid
from django.db import models

from django.conf import settings

from wine.models import Wine


class Cart(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "active"
        DONE = "done"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="carts"
    )
    status = models.CharField(
        max_length=64,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"cart {self.id} {self.status}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "wine"],
                name="unique_wine_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.quantity} - {self.wine.name}"
