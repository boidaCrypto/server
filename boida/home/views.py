from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange, Asset, Transaction
from home.calculate import upbit_home
from home.serializers import AssetSerializer, ConnectedExchangeSerializer
from transaction.function import transaction_func



# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def List(request, format=None):
    ### 연결된 데이터가 없을 경우, no data onboarding page
    user = request.data['user_id']
    connected_exchange = ConnectedExchange.objects.filter(user=user)
    if list(connected_exchange) == []:
        # 204이면, 연결된 거래소가 없음을 나타냄.
        return Response(status=status.HTTP_204_NO_CONTENT)

    ### 연결된 데이터가 있을 경우, Home page
    user = User.objects.get(pk=request.data["user_id"])
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

    result = transaction_func(transaction)
    # price : 체결가격, executed_volume : 체결수량, executed_price : 체결가격,
    response = {
        "connected_exchange": result[0],
        "transaction": result[1]
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





@api_view(['POST'])
@permission_classes([AllowAny])
def Test(request, format=None):
    import boto3
    AWS_ACCESS_KEY_ID = 'AKIARZNCNJPLGWSFJJG7'
    AWS_SECRET_ACCESS_KEY = '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'

    coin_name = "inj".upper()

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = s3_client.upload_file(
        "C:/Users/qudrh/Documents/GitHub/server/boida/" + coin_name + ".jpg",
        "boida",
        "crypto/image/" + coin_name + "/explain/" + coin_name + ".png"

    )


    return Response(status=status.HTTP_200_OK)