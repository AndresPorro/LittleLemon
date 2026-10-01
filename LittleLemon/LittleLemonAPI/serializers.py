from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username']


class CartMenuItemsSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menuitem', write_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    menuitems = OrderItemSerializer(
        many=True,
        source='orderitem_set',
        read_only=True,
    )
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Delivery Crew'),
        source='delivery_crew',
        write_only=True,
        required=False,
        allow_null=True,
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id','user','delivery_crew_id','delivery_crew','status','date','menuitems','total',]
        read_only_fields = ['id','user','delivery_crew','date','menuitems','total',]


class DeliveryCrewOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']