from django.urls import path
from .views import register, login

urlpatters = [
    path('register/', register, name='register'),
    path('login/', login, name='login')
]
