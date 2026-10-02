from django.db import transaction
# DRF Imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# Serializer Imports
from .serializers import MenuItemSerializer, CartMenuItemsSerializer, UserSerializer, OrderSerializer, DeliveryCrewOrderUpdateSerializer, CategorySerializer
# Models Imports
from .models import MenuItem, Cart, Order, Category
# DJANGO Imports
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
# Pagination Imports
from django.core.paginator import Paginator, EmptyPage
# Create your views here.


def is_customer(user):
    return not user.groups.filter(name__in=['Manager', 'Delivery Crew']).exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_delivery_crew(user):
    return user.groups.filter(name='Delivery Crew').exists()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def MenuItems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', 4)
        page = request.query_params.get('page', 1)

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(page)
        except EmptyPage:
            items = []
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def MenuItemsId(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'GET':
        return Response(MenuItemSerializer(item).data, status=status.HTTP_200_OK)

    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    if request.method in ('PUT', 'PATCH'):
        serializer = MenuItemSerializer(item, data=request.data,partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response({'message': 'Elemento eliminado'}, status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def GroupsManagerUsers(request):
    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        managers = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.validated_data['username'])
        manager_group = get_object_or_404(Group, name='Manager')
        user.groups.add(manager_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def GroupsManagerUsersId(request, pk):
    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=pk)
    manager_group = get_object_or_404(Group, name='Manager')
    user.groups.remove(manager_group)
    return Response({'message': 'Usuario eliminado del grupo Manager'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def DeliveryCrew(request):
    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        crew = User.objects.filter(groups__name='Delivery Crew')
        return Response(UserSerializer(crew, many=True).data, status=status.HTTP_200_OK)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.validated_data['username'])
        delivery_group = get_object_or_404(Group, name='Delivery Crew')
        user.groups.add(delivery_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeliveryCrewId(request, pk):
    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(User, pk=pk)
    delivery_group = get_object_or_404(Group, name='Delivery Crew')

    if not user.groups.filter(pk=delivery_group.pk).exists():
        return Response({'error': 'El usuario no es Delivery Crew'}, status=status.HTTP_404_NOT_FOUND)

    user.groups.remove(delivery_group)
    return Response({'message': 'Usuario eliminado del grupo Delivery Crew'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def CartMenuItems(request):
    if not is_customer(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if Cart.objects.filter(user=request.user).exists(): 
            carts = Cart.objects.filter(user=request.user)
            return Response(CartMenuItemsSerializer(carts, many=True).data, status=status.HTTP_200_OK)
        else: 
            return Response({'error': 'El carrito está vacío'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CartMenuItemsSerializer(data=request.data)
        if serializer.is_valid():
            menuitem = serializer.validated_data['menuitem']
            quantity = serializer.validated_data['quantity']
            cart_item, created = Cart.objects.update_or_create(
                user=request.user,
                menuitem=menuitem,
                defaults={
                    'quantity': quantity,
                    'unit_price': menuitem.price,
                    'price': menuitem.price * quantity,
                },
            )
            return Response(
                CartMenuItemsSerializer(cart_item).data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    Cart.objects.filter(user=request.user).delete()
    return Response({'message': 'Carrito vaciado'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Orders(request):
    if request.method == 'GET':
        if is_manager(request.user):
            orders = Order.objects.all()
        elif is_delivery_crew(request.user):
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)

    if not is_customer(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)
    
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        total_price = sum(item.price for item in cart_items)
        order = Order.objects.create(user=request.user, total=total_price)
        for item in cart_items:
            order.orderitem_set.create(
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price,
            )
    cart_items.delete()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def OrdersId(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'GET':
        if is_manager(request.user) or order.user == request.user or order.delivery_crew == request.user:
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        if is_manager(request.user):
            order.delete()
            return Response({'message': 'Pedido eliminado'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)


    if request.method in ('PUT', 'PATCH'):
        if is_manager(request.user):
            serializer = OrderSerializer(order, data=request.data, partial=(request.method == 'PATCH'))
        elif is_delivery_crew(request.user) and order.delivery_crew == request.user and request.method == 'PATCH':
            serializer = DeliveryCrewOrderUpdateSerializer(order, data=request.data, partial=True)
        else:
            return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def CategoriesView(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)
    
    if not is_manager(request.user):
        return Response({'error': 'No tienes permiso'}, status=status.HTTP_403_FORBIDDEN)
        
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)