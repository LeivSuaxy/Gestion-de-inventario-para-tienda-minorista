from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
      path('objects/', views.get_objects, name='get_objects'),
      path('insertstorage/', views.insert_storage_in_database, name='insert_storage'),
      path('total_objects/', views.get_total_objects, name='get_total_objects'),
      path('insertinventory/', views.insert_inventory_at_database, name='insert_inventory'),
      path('purchaseproducts/', views.process_buy_order, name='purchase_products'),
      path('search/', views.get_objects_by_name, name='search_products'),
      path('testcount/', views.get_objects_by_name, name='process_buy_order'),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
