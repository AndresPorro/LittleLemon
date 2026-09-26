from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured']