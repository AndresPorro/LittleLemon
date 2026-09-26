# DRF Imports
from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response
# Serializer Imports
from .serializers import MenuItemSerializer
# Models Imports
from .models import MenuItem
# Create your views here.

@api_view()
def MenuItems(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, 403)

@api_view(['GET'])
def MenuItemId(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, 403)