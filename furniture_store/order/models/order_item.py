from django.db import models
from product.models import Product
from cart.models.cart import Cart
from .order import Order

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(order__isnull=False, cart__isnull=True) |
                    models.Q(order__isnull=True, cart__isnull=False)
                ),
                name="orderitem_cart_or_order"
            ),
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_product_per_cart'
            ),
        ]

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    @property
    def total_price(self):
        unit_price = self.price or self.product.price
        return unit_price * self.quantity
    