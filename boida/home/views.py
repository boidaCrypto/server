import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def List(request, format=None):
    # 유저와 연동한 거래소들을 가져온다.

    # 현재 자산들을 계산한다.

    # 계산한 값들을 Firestore에 저장한다.

    # 계산한 값들을 보내준다.
    return Response(status=status.HTTP_200_OK)
