from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Test(request, format=None):
    # 현재 활동중인 User를 가져온다.
    now_active_user = User.objects.filter(now_active=True)
    print(now_active_user)
    # 활동중이면서, UPBIT 거래소를 연동한
    # User.objects.extra(tables=['connected_exchange'], where=[''])
    print(now_active_user.objects.extra(tables=['connected_exchange'], where=['exchange_id=1']))

    return Response(status=status.HTTP_200_OK)
