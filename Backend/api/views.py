from .models import StockElement
from .serializer import StockElementSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
import math


# Create your views here.
class TenItemsPaginator(PageNumberPagination):
    page_size: int = 5


class StockElementViewSet(viewsets.ModelViewSet):
    queryset = StockElement.objects.all()
    serializer_class = StockElementSerializer
