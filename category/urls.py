from django.urls import path
from .views import create_category, list_category, edit_category, delete_category

urlpatterns = [
    path('create-category/', create_category, name="create_category"),
    path('list-category/', list_category, name="list_category"),
    path('edit-category/<int:pk>/', edit_category, name="edit_category"),
    path('category/<int:pk>/delete/', delete_category, name="delete_category"),
]
