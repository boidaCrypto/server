from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def LocalRegister(request, format=None):
    return Response({"msg": "완료!"}, status=status.HTTP_200_OK)
