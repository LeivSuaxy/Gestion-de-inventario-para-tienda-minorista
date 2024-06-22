from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apiadmin import views

urlpatterns = [
    path('objects/', views.get_all_products, name='get_all_products'),
    path('employees/', views.get_all_employees, name='get_all_employees'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
