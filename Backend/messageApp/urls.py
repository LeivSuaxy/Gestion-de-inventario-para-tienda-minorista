from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('send_email/', views.send_email, name='send_email'),
    path('contact/', views.send_contact_email, name='send_contact_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)