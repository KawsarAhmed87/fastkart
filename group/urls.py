from django.urls import path
from .views import *

urlpatterns = [
    path('group-create', group_create, name="group_create"),
    path('group-list', group_list, name="group_list"),
    path('group-update/<int:group_id>', group_update, name="group_update"),
    path('group-delete/<int:group_id>', group_delete, name="group_delete"),
]