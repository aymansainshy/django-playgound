from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .controllers import register_controller, login_controller
from .serializers import UserResponseSerializer


# class RegisterView(generics.GenericAPIView):
#     userSerializer = UserResponseSerializer
#
#     def post(self, request):
#         return register_controller.register(self.request)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        pass


@api_view(['POST'])
def register(request):
    return register_controller.register(request)


@api_view(['POST'])
def login(request):
    return login_controller.login(request)


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def testToken(request):
    return Response({"passed!"})
