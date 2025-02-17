from django.urls import path
from .views import *

urlpatterns = [
    path('create-product/', create_product, name='create_product'),
    path('list-product/', list_product, name='list_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('view-product/<int:id>/', view_product, name='view_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),

    path('product/<int:product_id>/create-variant', create_product_variant, name='create_product_variant'),
    path('product/<int:product_id>/variants/', list_product_variants, name='list_product_variants'),
    path('product/<int:product_id>/variant/<int:variant_id>/edit/', edit_product_variant, name='edit_product_variant'),
    path('product/<int:product_id>/variant/<int:variant_id>/view/', view_product_variant, name='view_product_variant'),
    path('product/variant/<int:variant_id>/delete/', delete_product_variant, name='delete_product_variant'),

]
