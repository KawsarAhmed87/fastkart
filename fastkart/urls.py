from django.contrib import admin
from django.urls import path, include
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    

    path('dashboard', dashboard, name="dashboard"),
    path('', include('user.urls')),
    path('', include('group.urls')),
    path('', include('role.urls')),
    path('', include('category.urls')),
    path('', include('brand.urls')),
    path('', include('supplier.urls')),
    path('', include('attribute.urls')),
    path('', include('product.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)