import uuid
from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True
    )
    
    guest_id = models.CharField(
    max_length=255,  
    null=True,
    blank=True,
    db_index=True
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user.email if self.user else self.guest_id
        return f"Cart of {owner}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
