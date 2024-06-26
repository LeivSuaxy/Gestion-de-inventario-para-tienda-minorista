from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # <--Products CRUD URLS-->
    path('products/', views.get_all_products, name='get_all_products'),
    path('insert_product/', views.insert_product_in_database, name='insert_product'),
    path('update_product/', views.update_product_in_database, name='update_product'),
    path('delete_product/', views.delete_product_in_database, name='delete_product'),
    path('delete_products/', views.delete_products_in_database, name='delete_products'),
    # <--Employees CRUD URLS-->
    path('employees/', views.get_all_employees, name='get_all_employees'),
    path('insert_employee/', views.insert_employee_to_database, name='insert_employee'),
    path('update_employee/', views.update_employee_in_database, name='update_employee'),
    path('delete_employee/', views.delete_employee_in_database, name='delete_employee'),
    # <--Inventories CRUD URLS-->
    path('inventories/', views.get_all_inventories, name='get_all_inventories'),
    path('insert_inventory/', views.insert_inventory_in_database, name='insert_inventory'),
    path('delete_inventory/', views.delete_inventory_from_database, name='delete_inventory'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
