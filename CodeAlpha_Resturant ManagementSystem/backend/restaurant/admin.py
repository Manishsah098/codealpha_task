from django.contrib import admin
from .models import Inventory, MenuItem, RecipeRequirement, Table, Reservation, Order, OrderItem

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'threshold')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name',)

@admin.register(RecipeRequirement)
class RecipeRequirementAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'inventory', 'quantity_required')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'date_time', 'number_of_guests', 'status')
    list_filter = ('status', 'date_time')
    search_fields = ('customer_name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'table', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('total_amount',)
