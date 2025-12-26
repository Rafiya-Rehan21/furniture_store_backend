from rest_framework import serializers
from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_title',
            'product_image',
            'quantity',
            'price',
            'total_price'
        ]
        read_only_fields = ['id', 'price', 'total_price']

    def get_product_image(self, obj):
        if hasattr(obj.product, 'images') and obj.product.images.exists():
            first_image = obj.product.images.first()
            if first_image and first_image.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(first_image.image.url)
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    items_count = serializers.SerializerMethodField()
    full_address = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_email',
            'street_address',
            'city',
            'state',
            'postal_code',
            'country',
            'full_address',
            'status',
            'total_price',
            'items',
            'items_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'total_price',
            'created_at',
            'updated_at'
        ]

    def get_items_count(self, obj):
        return obj.items.count()


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for order list"""
    items_count = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user_email',
            'city',
            'state',
            'country',
            'status',
            'total_price',
            'items_count',
            'created_at'
        ]
        read_only_fields = fields

    def get_items_count(self, obj):
        return obj.items.count()


class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    def validate_status(self, value):
        order = self.context.get('order')
        
        valid_transitions = {
            Order.STATUS_PENDING: [Order.STATUS_PAID, Order.STATUS_CANCELLED],
            Order.STATUS_PAID: [Order.STATUS_SHIPPED, Order.STATUS_CANCELLED],
            Order.STATUS_SHIPPED: [Order.STATUS_DELIVERED],
            Order.STATUS_DELIVERED: [],
            Order.STATUS_CANCELLED: []
        }
        
        current_status = order.status
        
        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot transition from {current_status} to {value}"
            )
        
        return value
    