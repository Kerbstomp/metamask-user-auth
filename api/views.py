from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializers import UserSerializer
from .utils import MessageVerifier, JWTGenerator, get_new_nonce


api_routes = [
    {
        'Endpoint': '/auth/',
        'method': 'POST',
        'body': {
            'public_address (required)': '',
            'signature (required)': '',
        },
        'description': 'Attempts to authenticate a user with the provided public address and signature. On success, returns a JWT access token',
    },
    {
        'Endpoint': '/users/',
        'method': 'GET',
        'query_params': {
            'parameter': 'public_address',
            'required/optional': 'required',
            'type': 'text',
        },
        'body': None,
        'description': 'Returns a user, if exists, with the provided public address',
    },
    {
        'Endpoint': '/users/',
        'method': 'POST',
        'body': {
            'public_address (required)': '',
            'username (optional)': '',
        },
        'description': 'Creates a new user with the provided public address and username',
    },
]


@api_view(['GET'])
def get_routes(request) -> Response:
    return Response(api_routes)


@api_view(['POST'])
def authenticate_user(request) -> Response:
    try:
        public_address = request.data['public_address']
        signature = request.data['signature']
    except:
        return Response('Expected public_address and signature in the request body', status=400)

    try:
        user = User.objects.get(public_address=public_address)
        serializer = UserSerializer(user, many=False)
        nonce = serializer.data['nonce']
    except User.DoesNotExist:
        return Response('User with the provided public_address does not exist', status=404)

    message = 'I am signing my one-time nonce: {}'.format(nonce) # MOVE THIS SOMEWHERE ELSE, ENV VARS
    message_verifier = MessageVerifier(public_address, message, signature)
    message_verified = message_verifier.execute_message_verifier()
    
    if message_verified:
        user.nonce = get_new_nonce()
        user.save()

        jwt_generator = JWTGenerator(serializer.data['id'], serializer.data['public_address'])

        return Response({"access_token": jwt_generator.get_jwt_token()})
    else:
        return Response('Signature verification failed', status=401)


class UsersView(APIView):
    def get(self, request) -> Response:
        public_address = request.GET.get('public_address')
        # Add check to make sure address is valid ETH address
        # web3.is_address(public_address)
        if public_address is None or public_address == '':
            return Response('No public_address provided in query', status=400)
            
        try:
            user = User.objects.get(public_address=public_address)
            serializer = UserSerializer(user, many=False)
        except User.DoesNotExist:
            return Response('User with the provided public_address does not exist', status=404)

        return Response(serializer.data)

    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
