from django.db import models

class Inventory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10.0)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    restaurant_name = models.CharField(max_length=100, default='RMS Local')
    restaurant_address = models.CharField(max_length=200, default='123 Developer Lane')
    image_url = models.URLField(max_length=600, default='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80')
    is_veg = models.BooleanField(default=True)
    cuisine = models.CharField(max_length=100, default='General')

    def __str__(self):
        return self.name

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='requirements')
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity_required} of {self.inventory.name} for {self.menu_item.name}"

class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    number_of_guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.date_time}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.table:
            return f"Order #{self.id} (Table {self.table.number})"
        return f"Order #{self.id} (Table N/A)"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} for Order #{self.order.id}"
