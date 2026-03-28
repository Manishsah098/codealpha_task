import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rms_project.settings')
django.setup()

from restaurant.models import Inventory, MenuItem, RecipeRequirement, Table

def run():
    print("Clearing database...")
    RecipeRequirement.objects.all().delete()
    MenuItem.objects.all().delete()
    Inventory.objects.all().delete()
    Table.objects.all().delete()

    print("Creating Tables...")
    for i in range(1, 11):
        Table.objects.create(number=i, capacity=4 if i <= 5 else 6)

    print("Creating Inventory...")
    bun = Inventory.objects.create(name="Premium Bun", quantity=100, threshold=20)
    patty = Inventory.objects.create(name="Angus Beef Patty", quantity=50, threshold=15)
    cheese = Inventory.objects.create(name="Cheddar Cheese", quantity=200, threshold=30)
    lettuce = Inventory.objects.create(name="Fresh Lettuce", quantity=150, threshold=20)
    sauce = Inventory.objects.create(name="Secret Sauce", quantity=300, threshold=50)

    # Some Low Inventory
    truffle = Inventory.objects.create(name="Truffle Oil", quantity=2, threshold=5)

    print("Creating Menu Items & Recipes...")
    
    classic = MenuItem.objects.create(name="Classic Angus Burger", description="Our signature beef patty, cheddar, lettuce, and secret sauce.", price=12.99)
    RecipeRequirement.objects.create(menu_item=classic, inventory=bun, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=classic, inventory=patty, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=classic, inventory=cheese, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=classic, inventory=lettuce, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=classic, inventory=sauce, quantity_required=1)

    truffle_burger = MenuItem.objects.create(name="Truffle Mushroom Burger", description="Exquisite truffle infused burger for fine dining.", price=18.99)
    RecipeRequirement.objects.create(menu_item=truffle_burger, inventory=bun, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=truffle_burger, inventory=patty, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=truffle_burger, inventory=truffle, quantity_required=1)

    double = MenuItem.objects.create(name="Double Trouble", description="Two patties, double cheese, maximum flavor.", price=16.99)
    RecipeRequirement.objects.create(menu_item=double, inventory=bun, quantity_required=1)
    RecipeRequirement.objects.create(menu_item=double, inventory=patty, quantity_required=2)
    RecipeRequirement.objects.create(menu_item=double, inventory=cheese, quantity_required=2)

    print("Database Population Complete!")

if __name__ == "__main__":
    run()
