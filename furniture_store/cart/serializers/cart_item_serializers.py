from rest_framework import serializers
from order.models import OrderItem
from cart.models import Cart
from product.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.SerializerMethodField()
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
            'product_price',
            'product_image',
            'quantity',
            'price',
            'total_price'
        ]
        read_only_fields = ['id', 'price', 'total_price']

    def get_product_price(self, obj):
        """Get the current product price or variant price"""
        if hasattr(obj.product, 'variants') and obj.product.variants.exists():
            # Get first variant price as default
            return str(obj.product.variants.first().price)
        return "0.00"

    def get_product_image(self, obj):
        """Get product image URL"""
        if hasattr(obj.product, 'images') and obj.product.images.exists():
            first_image = obj.product.images.first()
            if first_image and first_image.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(first_image.image.url)
        return None

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        if value > 999:
            raise serializers.ValidationError("Quantity cannot exceed 999")
        return value

    def validate_product(self, value):
        if not hasattr(value, 'available') or value.available != 'in':
            raise serializers.ValidationError("This product is not available")
        if hasattr(value, 'items_in_stock') and value.items_in_stock <= 0:
            raise serializers.ValidationError("This product is out of stock")
        return value


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1, max_value=999)

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, available='in')
            if hasattr(product, 'items_in_stock') and product.items_in_stock <= 0:
                raise serializers.ValidationError("Product is out of stock")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or not available")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=999)
    