from django.test import TestCase
from .models import MenuItem
from .serializer import MenuItemSerializer
# Create your tests here.
class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")

class MenuViewTest(TestCase):
    def setUp(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        item1 = MenuItem.objects.create(title="Cream", price=80, inventory=100)

    def  test_getall(self): 
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        response = self.client.get("/menu/")
        self.assertEqual(response.data, serializer.data)