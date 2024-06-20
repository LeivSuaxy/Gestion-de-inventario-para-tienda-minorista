"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views as api_views
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('login.urls')),
    path('api/objects/', api_views.get_objects, name='get_objects'),
    path('api/insertstorage/', api_views.insert_storage_in_database, name='insert_storage'),
    path('api/total_objects/', api_views.get_total_objects, name='get_total_objects'),
    path('api/insertinventory/', api_views.insert_inventory_at_database, name='insert_inventory'),
    path('api/insertproduct/', api_views.insert_product_in_database, name='insert_product'),
    path('api/updateproduct/', api_views.update_product_in_database, name='update_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
