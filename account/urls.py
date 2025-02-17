from django.urls import path
from .views import create_account, list_account, edit_account, delete_account

urlpatterns = [
    path('create-account/', create_account, name="create_account"),
    path('list-account/', list_account, name="list_account"),
    path('edit-account/<int:pk>/', edit_account, name="edit_account"),
    path('account/<int:pk>/delete/', delete_account, name="delete_account"),
]
