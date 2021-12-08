import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange
from home.calculate import home
# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def List(request, format=None):
    #
    user = User.objects.get(pk=request.data["user"])
    # 유저와 연동한 거래소들을 가져온다.
    connected_exchange = ConnectedExchange.objects.filter(user=user)
    # 현재 자산들을 계산한다.
    for i in connected_exchange:
        print(i.access_key, i.secret_key)

        print(i)
        if i.exchange.exchange_name == "upbit":
            home(i.access_key, i.secret_key)


            response = {
                ""
            }

    # 계산한 값들을 Firestore에 저장한다.

    # 계산한 값들을 보내준다.
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def CheckConnectedExchange(request, format=None):
    user = request.data['user_id']
    connected_exchange = ConnectedExchange.objects.filter(user=user)

    if list(connected_exchange) == []:
        # 204이면, 연결된 거래소가 없음을 나타냄.
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        # 200이면, 연결된 거래소가 존재
        return Response(status=status.HTTP_200_OK)