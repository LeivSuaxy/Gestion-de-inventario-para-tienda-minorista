from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import Token
from .serializer import UserSerializer
from Backend.crudDB import CrudDB


# Create your views here.
# Register endpoint
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
    response = db.register_user(username=username, password=password)

    # If the registration is successful, return a 200 status
    if response == 200:
        return Response({'status': 'Success'}, status.HTTP_200_OK)
    # If the user already exists, return a 409 status
    elif response == 409:
        return Response({'status': 'This user already exists'}, status.HTTP_409_CONFLICT)
    # If there is any other error, return a 400 error
    else:
        return Response({'status': 'Error'}, status.HTTP_400_BAD_REQUEST)


# Login endpoint
@api_view(['POST'])
def login(request):
    """
    This view handles the login of a user.

    It expects a POST request with 'username' and 'password' in the request data.
    Responses:
    If the username or password is missing, it returns a 400 error.
    If the username does not exist in the database it returns a 409 error.
    If the password does not match the stored password for the user, it returns a 400 error.
    If the login is successful, it returns a 200 status.

    :param request: The request object
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

    # Call the log_in_user method of the CrudDB instance with the username and password
    response = db.log_in_user(username=username, password=password)

    # If the login is successful, return a 200 status
    if response == 200:
        return Response({'success': 'The user was founded'}, status.HTTP_200_OK)
    # If the user does not exist, return a 409 status
    elif response == 409:
        return Response({'not_found': "Please provide a username that's exists"}, status.HTTP_409_CONFLICT)
    # If the password does not match the stored password for the user, return a 400 error
    else:
        return Response({'error': 'The password is wrong'}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check(request):
    return Response({})
