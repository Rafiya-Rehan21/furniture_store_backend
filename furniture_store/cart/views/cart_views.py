import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from cart.models import Cart
from cart.serializers import CartSerializer


class CartViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing cart operations
    """
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user, is_active=True)
        
        guest_id = self.request.session.get('guest_id')
        if guest_id:
            return Cart.objects.filter(guest_id=guest_id, is_active=True)
        
        return Cart.objects.none()

    def get_or_create_cart(self):
        """Get or create cart for authenticated or guest user"""
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=self.request.user,
                is_active=True
            )
            return cart
        
        guest_id = self.request.session.get('guest_id')
        
        if not guest_id:
            guest_id = str(uuid.uuid4())
            self.request.session['guest_id'] = guest_id
        
        cart, created = Cart.objects.get_or_create(
            guest_id=guest_id,
            is_active=True
        )
        
        return cart

    def retrieve(self, request, *args, **kwargs):
        """Get current user's cart"""
        cart = self.get_or_create_cart()
        serializer = self.get_serializer(cart)
        
        response_data = serializer.data
        if not request.user.is_authenticated:
            response_data['guest_id'] = request.session.get('guest_id')
        
        return Response(response_data)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = self.get_or_create_cart()
        cart.items.filter(order__isnull=True).delete()
        
        serializer = self.get_serializer(cart)
        return Response(
            {
                'message': 'Cart cleared successfully',
                'cart': serializer.data
            },
            status=status.HTTP_200_OK
        )

                
    @action(detail=False, methods=['post'])
    def merge(self, request):
        """Merge guest cart with user cart after login"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'User must be authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Try to get guest_id from request data or session
        guest_id = request.data.get('guest_id') or request.session.get('guest_id')

        if not guest_id:
            return Response(
                {'error': 'guest_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            guest_cart = Cart.objects.get(guest_id=guest_id, is_active=True)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Guest cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user_cart, _ = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )

        for guest_item in guest_cart.items.filter(order__isnull=True):
            user_item = user_cart.items.filter(
                product=guest_item.product,
                order__isnull=True
            ).first()

            if user_item:
                user_item.quantity += guest_item.quantity
                user_item.save()
                guest_item.delete()
            else:
                guest_item.cart = user_cart
                guest_item.save()

        guest_cart.is_active = False
        guest_cart.save()

        serializer = self.get_serializer(user_cart)
        return Response(
            {
                'message': 'Carts merged successfully',
                'cart': serializer.data
            },
            status=status.HTTP_200_OK
        )
