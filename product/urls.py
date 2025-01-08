from django.urls import path
from .views import *

urlpatterns = [
    path('create-product/', create_product, name='create_product'),
    path('list-product/', list_product, name='list_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),
]
