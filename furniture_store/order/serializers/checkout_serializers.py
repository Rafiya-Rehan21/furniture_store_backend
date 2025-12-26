from rest_framework import serializers
from order.models import Order


class CheckoutSerializer(serializers.Serializer):
    street_address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)
    guest_id = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, data):
        request = self.context['request']
        
        if not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to checkout")
        
        return data
    