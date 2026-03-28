from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuItemViewSet, ReservationViewSet, place_order, 
    inventory_alerts, daily_sales_report, get_orders, update_order_status
)

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', place_order, name='place_order'),
    path('orders/all/', get_orders, name='get_orders'),
    path('orders/<int:pk>/status/', update_order_status, name='update_order_status'),
    path('inventory/alerts/', inventory_alerts, name='inventory_alerts'),
    path('reports/daily-sales/', daily_sales_report, name='daily_sales_report'),
]
