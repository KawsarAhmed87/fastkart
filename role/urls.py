from django.urls import path
from .views import *

urlpatterns = [
    path('role-create', role_create, name="role_create"),
    path('role-list', role_list, name="role_list"),
    path('role-update/<int:user_id>', role_update, name="role_update"),
    path('role-delete/<int:role_id>', role_delete, name="role_delete"),
]