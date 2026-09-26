from django.urls import path
# Views Imports
from . import views

urlpatterns = [ 
    path('menu-items/', views.MenuItems, name='MenuItems'),
    path('menu-items/<int:pk>/', views.MenuItemId, name='MenuItemId'),
]