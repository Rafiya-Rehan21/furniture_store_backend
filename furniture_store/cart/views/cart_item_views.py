from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from order.models import OrderItem
from cart.models import Cart
from product.models import Product
from cart.serializers import (
    CartItemSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing cart items
    """
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        cart = self.get_cart()
        if cart:
            return OrderItem.objects.filter(cart=cart, order__isnull=True).select_related('product')
        return OrderItem.objects.none()

    def get_cart(self):
        """Get cart for authenticated or guest user"""
        if self.request.user.is_authenticated:
            return Cart.objects.filter(
                user=self.request.user,
                is_active=True
            ).first()
        
        guest_id = self.request.session.get('guest_id')
        if guest_id:
            return Cart.objects.filter(
                guest_id=guest_id,
                is_active=True
            ).first()
        
        return None

    def get_or_create_cart(self):
        """Get or create cart"""
        import uuid
        
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                user=self.request.user,
                is_active=True
            )
            return cart
        
        guest_id = self.request.session.get('guest_id')
        
        if not guest_id:
            guest_id = str(uuid.uuid4())
            self.request.session['guest_id'] = guest_id
        
        cart, _ = Cart.objects.get_or_create(
            guest_id=guest_id,
            is_active=True
        )
        
        return cart

    def list(self, request, *args, **kwargs):
        """List all items in cart"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        total_price = sum(item.total_price for item in queryset)
        
        return Response({
            'items': serializer.data,
            'total_price': str(total_price),
            'items_count': queryset.count()
        })

    def create(self, request, *args, **kwargs):
        """Add item to cart"""
        add_serializer = AddToCartSerializer(data=request.data)
        add_serializer.is_valid(raise_exception=True)
        
        product_id = add_serializer.validated_data['product_id']
        quantity = add_serializer.validated_data['quantity']
        
        product = get_object_or_404(Product, id=product_id, available='in')
        cart = self.get_or_create_cart()
        
        cart_item = OrderItem.objects.filter(
            cart=cart,
            product=product,
            order__isnull=True
        ).first()
        
        if hasattr(product, 'variants') and product.variants.exists():
            product_price = product.variants.first().price
        else:
            product_price = 0
        
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
            message = 'Cart item quantity updated'
        else:
            cart_item = OrderItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price=product_price
            )
            message = 'Item added to cart'
        
        serializer = self.get_serializer(cart_item)
        
        return Response(
            {
                'message': message,
                'guest_id': cart.guest_id,  
                'item': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


    def update(self, request, *args, **kwargs):
        """Update cart item quantity"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        update_serializer = UpdateCartItemSerializer(data=request.data)
        update_serializer.is_valid(raise_exception=True)
        
        instance.quantity = update_serializer.validated_data['quantity']
        instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response({
            'message': 'Cart item updated successfully',
            'item': serializer.data
        })

    def partial_update(self, request, *args, **kwargs):
        """Partially update cart item"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Remove item from cart"""
        instance = self.get_object()
        instance.delete()
        
        return Response(
            {'message': 'Item removed from cart'},
            status=status.HTTP_204_NO_CONTENT
        )
        