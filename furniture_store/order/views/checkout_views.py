from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404

from order.models import Order, OrderItem
from cart.models import Cart
from order.serializers import CheckoutSerializer, OrderSerializer


class CheckoutViewSet(viewsets.GenericViewSet):
    """
    ViewSet for checkout operations
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSerializer
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """
        Create order from cart items
        Moves items from cart to order
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        street_address = serializer.validated_data['street_address']
        city = serializer.validated_data['city']
        state = serializer.validated_data['state']
        postal_code = serializer.validated_data['postal_code']
        country = serializer.validated_data['country']
        guest_id = serializer.validated_data.get('guest_id')
        
        cart = None
        if guest_id:
            cart = Cart.objects.filter(
                guest_id=guest_id,
                is_active=True
            ).first()
        
        if not cart:
            cart = Cart.objects.filter(
                user=request.user,
                is_active=True
            ).first()
        
        if not cart:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart_items = OrderItem.objects.filter(
            cart=cart,
            order__isnull=True
        ).select_related('product')
        
        if not cart_items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        total_price = sum(item.total_price for item in cart_items)
        
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    street_address=street_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    country=country,
                    status=Order.STATUS_PENDING,
                    total_price=total_price
                )
                
                for cart_item in cart_items:
                    if hasattr(cart_item.product, 'variants') and cart_item.product.variants.exists():
                        product_price = cart_item.product.variants.first().price
                    else:
                        product_price = 0
                    
                    cart_item.order = order
                    cart_item.cart = None
                    cart_item.price = product_price  
                    cart_item.save()
                
                if guest_id and cart.guest_id:
                    cart.is_active = False
                    cart.save()
                
                order_serializer = OrderSerializer(order, context={'request': request})
                
                return Response(
                    {
                        'message': 'Order created successfully',
                        'order': order_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
        
        except Exception as e:
            return Response(
                {'error': f'Failed to create order: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            