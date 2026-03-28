from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import Sum, Count, F

from .models import Inventory, MenuItem, Table, Reservation, Order, OrderItem
from .serializers import (
    InventorySerializer, MenuItemSerializer, TableSerializer,
    ReservationSerializer, OrderSerializer
)

class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/menu/
    """
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True)

class ReservationViewSet(viewsets.ModelViewSet):
    """
    POST /api/reservations/
    GET /api/reservations/
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        # basic availability check
        table_id = request.data.get('table')
        date_time_str = request.data.get('date_time')
        if not table_id or not date_time_str:
            return Response({'error': 'table and date_time required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils.dateparse import parse_datetime
        req_dt = parse_datetime(date_time_str)
        if not req_dt:
            return Response({'error': 'invalid date_time format'}, status=status.HTTP_400_BAD_REQUEST)

        # check if table is booked within 2 hours of this time
        time_threshold_start = req_dt - timedelta(hours=2)
        time_threshold_end = req_dt + timedelta(hours=2)
        
        overlapping = Reservation.objects.filter(
            table_id=table_id,
            status__in=['pending', 'confirmed'],
            date_time__gt=time_threshold_start,
            date_time__lt=time_threshold_end
        )
        if overlapping.exists():
            return Response({'error': 'Table is already reserved near this time'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)

@api_view(['POST'])
@transaction.atomic
def place_order(request):
    """
    POST /api/orders/
    Expected structure:
    {
      "table": 1,
      "items": [
        {"menu_item": 1, "quantity": 2},
        {"menu_item": 3, "quantity": 1}
      ]
    }
    """
    table_id = request.data.get('table')
    items_data = request.data.get('items', [])

    if not table_id or not items_data:
        return Response({'error': 'table and items are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        return Response({'error': 'invalid table'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total and check inventory
    total_amount = 0
    order_items_to_create = []
    inventory_deductions = {}

    for item in items_data:
        menu_item_id = item.get('menu_item')
        quantity = int(item.get('quantity', 1))

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id, is_available=True)
        except MenuItem.DoesNotExist:
            return Response({'error': f'MenuItem {menu_item_id} is invalid or unavailable'}, status=status.HTTP_400_BAD_REQUEST)

        price = menu_item.price
        total_amount += (price * quantity)

        # Log deductions based on recipes
        for req in menu_item.requirements.all():
            inv_id = req.inventory.id
            needed = req.quantity_required * quantity
            if inv_id in inventory_deductions:
                inventory_deductions[inv_id] += needed
            else:
                inventory_deductions[inv_id] = needed

        order_items_to_create.append({
            'menu_item': menu_item,
            'quantity': quantity,
            'price': price
        })

    # Verify we have enough inventory
    for inv_id, needed_qty in inventory_deductions.items():
        inv_item = Inventory.objects.select_for_update().get(id=inv_id)
        if inv_item.quantity < needed_qty:
            return Response({'error': f'Not enough inventory for {inv_item.name}. Need {needed_qty}, have {inv_item.quantity}'}, status=status.HTTP_400_BAD_REQUEST)

    # Deduct inventory
    for inv_id, needed_qty in inventory_deductions.items():
        inv_item = Inventory.objects.get(id=inv_id)
        inv_item.quantity -= needed_qty
        inv_item.save()

    import decimal
    # Apply 5% tax
    tax = total_amount * decimal.Decimal('0.05')
    grand_total = total_amount + tax

    # Create Order
    order = Order.objects.create(table=table, total_amount=grand_total, status='pending')

    for o_data in order_items_to_create:
        OrderItem.objects.create(
            order=order,
            menu_item=o_data['menu_item'],
            quantity=o_data['quantity'],
            price=o_data['price']
        )

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def inventory_alerts(request):
    """
    GET /api/inventory/alerts/
    """
    alerts = Inventory.objects.filter(quantity__lte=F('threshold'))
    serializer = InventorySerializer(alerts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_orders(request):
    """
    GET /api/orders/all/
    """
    orders = Order.objects.all().order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_order_status(request, pk):
    """
    PATCH /api/orders/<int:pk>/status/
    { "status": "preparing" }
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if not new_status:
        return Response({'error': 'status is required'}, status=status.HTTP_400_BAD_REQUEST)

    if new_status not in dict(Order.STATUS_CHOICES):
        return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET'])
def daily_sales_report(request):
    """
    GET /api/reports/daily-sales/
    """
    today = timezone.localdate()
    orders_today = Order.objects.filter(created_at__date=today, status__in=['completed', 'pending', 'preparing'])
    
    total_sales = orders_today.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    order_count = orders_today.count()

    return Response({
        'date': today,
        'total_sales': total_sales,
        'order_count': order_count
    })
