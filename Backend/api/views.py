from .models import StockElement
from .serializer import StockElementSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from Backend.crudDB import CrudDB, ResponseType


# Create your views here.
class TenItemsPaginator(PageNumberPagination):
    page_size: int = 5


class StockElementViewSet(viewsets.ModelViewSet):
    queryset = StockElement.objects.all()
    serializer_class = StockElementSerializer


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializador = StockElementSerializer(data=request.data, many=True)
        if serializador.is_valid():
            elements = serializador.validated_data

            email_body = '\n'.join(f'{element["name"]}: {element["price"]}' for element in elements)

            send_mail('Elementos', email_body, '', [''])
            return Response({'status': 'email sent'})
        else:
            return Response(serializador.errors, status=400)


@api_view(['GET'])
def get_objects(request):
    db = CrudDB()
    page = request.GET.get('page', 0)
    objects = db.get_response_elements(int(page))
    return objects


@api_view(['GET'])
def get_total_objects(request):
    db = CrudDB()
    objects = db.get_amount_elements_stock()
    return objects
