from django.urls import path
from .views import *


urlpatterns = [
    path ('create-purchase', create_purchase, name="create_purchase"),
    path ('list-purchase', list_purchase, name="list_purchase"),
    path ('view-purchase/<int:purchase_id>', view_purchase, name="view_purchase"),
    path ('edit-purchase/<int:id>', edit_purchase, name="edit_purchase"),
    path('purchase/<int:pk>/delete/', delete_purchase, name='delete_purchase'),
    
]