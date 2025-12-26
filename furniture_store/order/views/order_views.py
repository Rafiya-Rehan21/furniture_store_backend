from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from order.models import Order
from order.serializers import (
    OrderSerializer,
    OrderListSerializer,
    UpdateOrderStatusSerializer
)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing orders
    List, Retrieve, and Update Status operations
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items__product').order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """List all user orders"""
        queryset = self.get_queryset()
        
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'orders': serializer.data,
            'count': queryset.count()
        })
    
    def retrieve(self, request, *args, **kwargs):
        """Get order details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update order status (admin/staff only for most statuses)"""
        order = self.get_object()
        
        if not request.user.is_staff:
            if request.data.get('status') != Order.STATUS_CANCELLED:
                return Response(
                    {'error': 'Only staff can update order status'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if order.status not in [Order.STATUS_PENDING, Order.STATUS_PAID]:
                return Response(
                    {'error': 'Can only cancel pending or paid orders'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = UpdateOrderStatusSerializer(
            data=request.data,
            context={'order': order}
        )
        serializer.is_valid(raise_exception=True)
        
        order.status = serializer.validated_data['status']
        order.save()
        
        response_serializer = OrderSerializer(order, context={'request': request})
        
        return Response({
            'message': 'Order status updated successfully',
            'order': response_serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.status not in [Order.STATUS_PENDING, Order.STATUS_PAID]:
            return Response(
                {'error': f'Cannot cancel order with status: {order.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = Order.STATUS_CANCELLED
        order.save()
        
        serializer = OrderSerializer(order, context={'request': request})
        
        return Response({
            'message': 'Order cancelled successfully',
            'order': serializer.data
        })