import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import MenuItem

indian_foods = [
    ("Butter Chicken", "Rich and creamy tomato-based curry with tender chicken.", 14.99, 4.8),
    ("Chicken Tikka Masala", "Roasted marinated chicken chunks in spiced curry sauce.", 13.99, 4.7),
    ("Paneer Butter Masala", "Indian cottage cheese cooked in a rich tomato gravy.", 12.99, 4.6),
    ("Palak Paneer", "Fresh spinach pureed and cooked with cottage cheese.", 11.99, 4.5),
    ("Chana Masala", "Spicy and tangy chickpea curry.", 10.99, 4.4),
    ("Dal Makhani", "Slow-cooked black lentils with butter and cream.", 9.99, 4.7),
    ("Garlic Naan", "Soft flatbread baked in tandoor, topped with garlic.", 3.99, 4.9),
    ("Butter Naan", "Classic Indian tandoori bread with butter.", 2.99, 4.6),
    ("Jeera Rice", "Basmati rice cooked with cumin seeds.", 4.99, 4.3),
    ("Vegetable Biryani", "Aromatic basmati rice cooked with mixed vegetables and spices.", 11.99, 4.5),
    ("Chicken Biryani", "Classic layered rice dish with marinated chicken.", 14.99, 4.8),
    ("Samosa (2 pcs)", "Crispy pastry filled with spiced potatoes and peas.", 4.99, 4.7),
    ("Aloo Gobi", "Cauliflower and potatoes cooked with turmeric and spices.", 10.99, 4.4),
    ("Malai Kofta", "Potato and paneer balls in a creamy, rich gravy.", 12.99, 4.6),
    ("Gulab Jamun", "Fried dough balls soaked in sweet, sticky sugar syrup.", 3.99, 4.8)
]

print("Adding Indian food items...")
for name, desc, price, rating in indian_foods:
    item, created = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'description': desc,
            'price': price,
            'rating': rating,
            'cuisine': 'Indian',
            'restaurant_name': 'Spice of India',
            'restaurant_address': '456 Curry Lane'
        }
    )
    if created:
        print(f"Added {name}")
    else:
        print(f"{name} already exists.")

print("15 Indian food items added successfully!")
