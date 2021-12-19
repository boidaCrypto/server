import operator

import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange, Asset, Transaction
from home.calculate import upbit_home
from home.serializers import AssetSerializer, ConnectedExchangeSerializer

import numpy as np
import pandas as pd


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def List(request, format=None):
    #
    user = User.objects.get(pk=request.data["user"])
    # 유저와 연동한 거래소들을 가져온다.
    connected_exchange = ConnectedExchange.objects.filter(user=user)
    # 현재 업비트 자산들을 계산한다.
    for i in connected_exchange:
        if i.exchange.exchange_name == "upbit":
            # upbit asset 계산 후, DB 저장
            upbit_home(i.access_key, i.secret_key, user, i.exchange)
            # 저장된, upbit asset 가져오기.
            upbit_asset = Asset.objects.filter(user=user, exchange=i.exchange)
            upbit_asset = AssetSerializer(upbit_asset, many=True)

            response = {
                "total": [
                    {
                        "total_asset": 123,
                        "total_valuation_loss": 123,
                        "total_valuation_earning_rate": 123
                    }
                ],
                "exchange": [
                    upbit_asset.data
                ]
            }

    return Response(response, status=status.HTTP_200_OK)

    # 거래내역이 존재하지 않는 경우?


@api_view(['POST'])
@permission_classes([AllowAny])
def TotalAsset(request, format=None):
    # 최근 거래내역 5개 가져오기, 일자가 겹치는 것은 하나로 몰기., 현재는 업비트만 고려해서 불러온다.
    # 유저가 연동한 거래소의 아이디로 거래내역을 가져온다.
    connected_exchange = ConnectedExchange.objects.get(user=request.data["user_id"], exchange=1)
    transaction = Transaction.objects.filter(connected_exchange=connected_exchange).order_by("-created_at")[:5]

    # 일자별로 분류하기
    transaction = pd.DataFrame(
        transaction.values("id", "connected_exchange_id", "side", "price", "market", "executed_volume",
                           "created_at"))
    # year-month-day
    ymd = transaction["created_at"].dt.strftime("%Y-%m-%d")
    # hour-minute
    hm = transaction["created_at"].dt.strftime("%H:%M")
    transaction["ymd"] = ymd
    transaction["hm"] = hm
    # 얼마 샀는지
    transaction["executed_price"] = transaction["price"] * transaction["executed_volume"]

    # 날짜 중복 제거
    common_created_at = ymd.drop_duplicates(keep='first')
    result = []
    for i in common_created_at:
        data1 = transaction[transaction["ymd"] == i].to_dict(orient='records')
        data2 = {"date": i, "data": data1}
        result.append(data2)

    # 거래소 정보 가져오기.
    exchange_id = transaction["connected_exchange_id"].drop_duplicates(keep='first').values
    connected_exchange = ConnectedExchange.objects.filter(id__in=exchange_id, is_deleted=False)
    connected_exchange = ConnectedExchangeSerializer(connected_exchange, many=True)

    # price : 체결가격, executed_volume : 체결수량, executed_price : 체결가격,
    response = {
        "connected_exchange": connected_exchange.data,
        "transaction": result
    }

    return Response(response, status.HTTP_200_OK)


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
