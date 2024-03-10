from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .controllers import register_controller, login_controller


@api_view(['POST'])
def register(request):
    return register_controller.register(request)


@api_view(['POST'])
def login(request):
    return login_controller.login(request)


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"passed!"})