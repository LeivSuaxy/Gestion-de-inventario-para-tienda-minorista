from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import Token
from .serializer import UserSerializer
from Backend.crudDB import CrudDB as db


# Create your views here.

@api_view(['POST'])
def register(request):
    print(request.data)
    dp = db()
    dp.connect_test()
    return Response({'Hello'}, status=200)


@api_view(['POST'])
def login(request):
    return Response({})


@api_view(['POST'])
def check(request):
    return Response({})
