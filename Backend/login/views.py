from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import Token
from .serializer import UserSerializer
from Backend.crudDB import CrudDB


# Create your views here.

@api_view(['POST'])
def register(request):
    """
    This view handles the registration of a new user

    It expects a POST request with 'username' and 'password' in the request data.
    If the username or password is missing, it returns a 400 error.
    If the username already exists in the database it returns a 409 error.
    If the registration is successful, it returns a 200 status.

    :param request: The request object.
    :return: A response object with the status of the operation.
    """

    # Create a new instance of the CrudDB class
    db = CrudDB()

    # Try to get the username and password from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # If the username or password is not in the request, return a 400 error
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status.HTTP_400_BAD_REQUEST)

    # Call the register_user method of the CrudDB instance with the username and password
    responsedb = db.register_user(username=username, password=password)

    # If the registration is successful, return a 200 status
    if responsedb == 200:
        return Response({'status': 'Success'}, status.HTTP_200_OK)
    # If the user already exists, return a 409 status
    elif responsedb == 409:
        return Response({'status': 'This user already exists'}, status.HTTP_409_CONFLICT)
    # If there is any other error, return a 400 error
    else:
        return Response({'status': 'Error'}, status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    return Response({})


@api_view(['POST'])
def check(request):
    return Response({})
