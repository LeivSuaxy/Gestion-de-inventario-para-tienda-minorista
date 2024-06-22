from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apiadmin import views

urlpatterns = [
    path('elements/', views.get_all_products, name='get_all_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
