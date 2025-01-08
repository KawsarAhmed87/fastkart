from django.urls import path
from .views import *


urlpatterns = [
    path ('create-brand', create_brand, name="create_brand"),
    path ('list-brand', list_brand, name="list_brand"),
    path ('edit-brand/<int:id>', edit_brand, name="edit_brand"),
    path('brand/<int:pk>/delete/', delete_brand, name='delete_brand'),
    
]