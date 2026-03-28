from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from .models import Inventory, MenuItem, RecipeRequirement, Table, Reservation, Order

class RestaurantAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Setup Data
        self.inventory_bun = Inventory.objects.create(name='Bun', quantity=50, threshold=10)
        self.inventory_patty = Inventory.objects.create(name='Patty', quantity=30, threshold=10)
        
        self.burger = MenuItem.objects.create(name='Burger', price=Decimal('10.00'), is_available=True)
        RecipeRequirement.objects.create(menu_item=self.burger, inventory=self.inventory_bun, quantity_required=1)
        RecipeRequirement.objects.create(menu_item=self.burger, inventory=self.inventory_patty, quantity_required=1)
        
        self.table1 = Table.objects.create(number=1, capacity=4)

    def test_place_order_success(self):
        payload = {
            'table': self.table1.id,
            'items': [
                {'menu_item': self.burger.id, 'quantity': 2}
            ]
        }
        response = self.client.post(reverse('place_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().total_amount, Decimal('20.00'))
        
        # Check inventory deduction
        self.inventory_bun.refresh_from_db()
        self.inventory_patty.refresh_from_db()
        self.assertEqual(self.inventory_bun.quantity, Decimal('48.00'))
        self.assertEqual(self.inventory_patty.quantity, Decimal('28.00'))

    def test_place_order_insufficient_inventory(self):
        self.inventory_bun.quantity = 1
        self.inventory_bun.save()
        
        payload = {
            'table': self.table1.id,
            'items': [
                {'menu_item': self.burger.id, 'quantity': 2}
            ]
        }
        response = self.client.post(reverse('place_order'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_reservation_availability(self):
        req_time = timezone.now() + timedelta(days=1)
        
        # Make a reservation
        res1 = self.client.post(reverse('reservation-list'), {
            'table': self.table1.id,
            'customer_name': 'John',
            'date_time': req_time.isoformat(),
            'number_of_guests': 2,
            'status': 'confirmed'
        })
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        
        # Try to make overlapping reservation
        overlap_time = req_time + timedelta(hours=1)
        res2 = self.client.post(reverse('reservation-list'), {
            'table': self.table1.id,
            'customer_name': 'Jane',
            'date_time': overlap_time.isoformat(),
            'number_of_guests': 2
        })
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inventory_alerts(self):
        self.inventory_bun.quantity = 5 # Below threshold of 10
        self.inventory_bun.save()
        response = self.client.get(reverse('inventory_alerts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Bun')
