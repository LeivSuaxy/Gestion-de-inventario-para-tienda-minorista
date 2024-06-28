from django.shortcuts import render
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
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

    # Get info client
    name: str = info_client['name']
    email: str = info_client['email']

    if not __is_valid_email__(email):
        return Response({'error': 'Please provide a correct email'}, status.HTTP_400_BAD_REQUEST)

    # Get Products
    productos = [ProductoTemp(dat['name'], dat['price'], dat['quantity']) for dat in data]
    html_content = render_to_string('correo.html', context={'nombre': name, 'productos': productos})

    email_message: EmailMessage = EmailMessage('Hola, aqui esta tu pedido', body=html_content, to=[f'{email}'],
                                               from_email='elitestock970430@gmail.com')

    email_message.content_subtype = 'html'

    email_message.send()
    return render(request, 'correo.html', context={'nombre': name, 'productos': productos})


# New Method to send email to owners
@api_view(['POST'])
def send_contact_email(request):
    if not request.data.get('name') or not request.data.get('email') or not request.data.get('content'):
        return Response({'error': 'Por favor proporciona todos los campos requeridos',
                         'required_fields': 'name, email, content'}, status.HTTP_400_BAD_REQUEST)

    if not __is_valid_email__(request.data.get('email')):
        return Response({'error': 'Please provide a correct email'}, status.HTTP_400_BAD_REQUEST)

    targets = ['starterledfull@gmail.com']

    send_mail(subject=f'Un cliente {request.data.get("name")} le ha enviado un mensaje',
              message=request.data.get('content'),
              from_email=request.data.get('email'),
              recipient_list=targets)

    return Response({'status': 'Confirm'}, status.HTTP_200_OK)


def __is_valid_email__(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class ProductoTemp:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.total = self.precio * self.cantidad
