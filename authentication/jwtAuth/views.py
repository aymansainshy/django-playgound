from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from .controllers import register_controller, login_controller
from .models import User
from .serializers import UserResponseSerializer
from core.settings import SECRET_KEY
import jwt


# class RegisterView(generics.GenericAPIView):
#     userSerializer = UserResponseSerializer
#
#     def post(self, request):
#         return register_controller.register(self.request)

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.encode(token, SECRET_KEY)
            user = User.objects.get(payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


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
