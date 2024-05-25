from .models import StockElement
from .serializer import StockElementSerializer
from rest_framework import viewsets


# Create your views here.
class StockElementViewSet(viewsets.ModelViewSet):
    queryset = StockElement.objects.all()
    serializer_class = StockElementSerializer
