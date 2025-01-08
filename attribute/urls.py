from django.urls import path
from .views import create_attribute, list_attribute, edit_attribute, delete_attribute

urlpatterns = [
    path('create-attribute', create_attribute, name="create_attribute"),
    path('list-attribute', list_attribute, name="list_attribute"),
    path('edit-attribute/<int:id>', edit_attribute, name="edit_attribute"),
    path('attribute/<int:pk>/delete/', delete_attribute, name='delete_attribute'),
]
