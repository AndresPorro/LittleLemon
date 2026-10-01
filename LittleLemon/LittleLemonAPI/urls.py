from django.urls import path
# Views Imports
from . import views

urlpatterns = [ 
    path('menu-items/', views.MenuItems, name='MenuItems'),
    path('menu-items/<int:pk>/', views.MenuItemsId, name='MenuItemsId'),
    path('groups/manager/users/', views.GroupsManagerUsers, name='GroupsManagerUsers'),
    path('groups/manager/users/<int:pk>/', views.GroupsManagerUsersId, name='GroupsManagerUsersId'),
    path('groups/delivery-crew/users/', views.DeliveryCrew, name='DeliveryCrew'),
    path('groups/delivery-crew/users/<int:pk>/', views.DeliveryCrewId, name='DeliveryCrewId'),
    path('cart/menu-items/', views.CartMenuItems, name='CartMenuItems'),
    path('orders/', views.Orders, name='Orders'),
    path('orders/<int:pk>/', views.OrdersId, name='OrdersId'),
    path('categories/', views.CategoriesView, name='CategoriesView'),
]