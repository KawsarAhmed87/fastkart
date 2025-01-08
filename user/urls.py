from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register_page, name='register_page'),
    path ('login', login_page, name="login_page"),
    path ('login_process', login_process, name="login_process"),
    path ('logout', logout_page, name="logout_page"),
    path ('profile', profile, name="profile"),
    path('password/change/', change_password, name='change_password'),
    
]