from .models import StockElement
from .serializer import StockElementSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
class StockElementViewSet(viewsets.ModelViewSet):
    queryset = StockElement.objects.all()
    serializer_class = StockElementSerializer


@api_view(['GET'])
def count_elements(request):
    count: int = StockElement.objects.count()
    return Response({'count': count})
