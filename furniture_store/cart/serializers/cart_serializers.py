from rest_framework import serializers
from cart.models import Cart
from .cart_item_serializers import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'guest_id',
            'items',
            'items_count',
            'total_price',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'guest_id', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        return obj.items.filter(order__isnull=True).count()
    