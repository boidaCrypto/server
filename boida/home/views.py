import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def List(request, format=None):
    user = User.objects.get(pk=request.data["user"])
    # 유저와 연동한 거래소들을 가져온다.
    connected_exchage = ConnectedExchange.objects.filter(user=user)
    # 현재 자산들을 계산한다.
    for i in connected_exchage:
        if i.exchange.exchange_name == "upbit":
            print("upbit")
            response = {
                ""
            }

    # 계산한 값들을 Firestore에 저장한다.

    # 계산한 값들을 보내준다.
    return Response(status=status.HTTP_200_OK)
