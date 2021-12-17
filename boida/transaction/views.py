from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from users.models import User

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Test(request, format=None):
    # 현재 활동중인 User를 가져온다.
    now_active_user = User.objects.filter(now_active=True)
    print(now_active_user)
    # 활동중이면서, api를 연동한



    return Response(status=status.HTTP_200_OK)
