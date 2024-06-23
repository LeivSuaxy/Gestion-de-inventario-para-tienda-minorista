from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # <--Products CRUD URLS-->
    path('products/', views.get_all_products, name='get_all_products'),
    path('insert_products', views.insert_product_in_database, name='insert_product'),
    path('update_product', views.update_product_in_database, name='update_product'),
    path('delete_product', views.delete_product_in_database, name='delete_product'),
    # <--Employees CRUD URLS-->
    path('employees/', views.get_all_employees, name='get_all_employees'),
    path('insert_employee/', views.insert_employee_to_database, name='insert_employee'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
