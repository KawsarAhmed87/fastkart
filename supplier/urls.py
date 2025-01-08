from django.urls import path
from .views import *

urlpatterns = [
    path('create-supplier/', create_supplier, name='create_supplier'),
    path('list-supplier/', list_supplier, name='list_supplier'),
    path('edit-supplier/<int:id>/', edit_supplier, name='edit_supplier'),
    path('supplier/<int:id>/', view_supplier, name='view_supplier'),
    path('supplier/<int:pk>/delete/', delete_supplier, name='delete_supplier'),
]
