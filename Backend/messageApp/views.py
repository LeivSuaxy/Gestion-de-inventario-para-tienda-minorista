from django.shortcuts import render
from rest_framework.decorators import api_view


# Create your views here.
# TODO System of messages for the app and build the template.
@api_view(['GET'])
def send_email(request):
    nombre = 'Maria'

    return render(request, template_name='correo.html', context={'nombre': nombre})


class ProductoTemp:
    def __init__(self):
        self.nombre = 'Lapiz'
        self.precio = 30
        self.cantidad = 400
