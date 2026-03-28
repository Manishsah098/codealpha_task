from rest_framework import serializers
from .models import Inventory, MenuItem, RecipeRequirement, Table, Reservation, Order, OrderItem

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class RecipeRequirementSerializer(serializers.ModelSerializer):
    inventory_name = serializers.ReadOnlyField(source='inventory.name')

    class Meta:
        model = RecipeRequirement
        fields = ['id', 'inventory', 'inventory_name', 'quantity_required']

class MenuItemSerializer(serializers.ModelSerializer):
    requirements = RecipeRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'is_available', 'rating', 'restaurant_name', 'restaurant_address', 'image_url', 'is_veg', 'cuisine', 'requirements']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'quantity', 'price']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'status', 'total_amount', 'created_at', 'items']
        read_only_fields = ['total_amount', 'created_at']
