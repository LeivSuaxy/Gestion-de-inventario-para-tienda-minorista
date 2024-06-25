from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
# TODO System of messages for the app and build the template.
@api_view(['POST'])
def send_email(request):
    info_client = request.data.get('client')
    data = request.data.get('products')

    if not info_client or not data:
        return Response({'error': 'Please provide client and products data'}, status.HTTP_400_BAD_REQUEST)

    print(info_client)
    # Get info client
    name: str = info_client['name']
    email: str = info_client['email']

    # Get Products

    print(data)
    print(info_client)
    print(type(data))
    print(type(info_client))

    productos = [ProductoTemp(dat['name'], dat['price'], dat['quantity']) for dat in data]
    html_content = render_to_string('correo.html', context={'nombre': name, 'productos': productos})

    email_message: EmailMessage = EmailMessage('Hola, aqui esta tu pedido', body=html_content, to=[f'{email}'], from_email='elitestock970430@gmail.com')

    email_message.content_subtype = 'html'

    email_message.send()
    return render(request, 'correo.html', context={'nombre': name, 'productos': productos})



class ProductoTemp:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.total = self.precio * self.cantidad
