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
    user_info = User.objects.get(id=user)

    # 현재는 업비트 대상으로만 api

    # 연동된 거래소가 없을 경우.
    try:
        connected_exchange = ConnectedExchange.objects.get(user=user, is_deleted=False)
    except Exception as e:
        print(e, "{0}님의 연동된 거래소가 없습니다.".format(user_info.nickname))
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 거래소 이름
    connected_exchange_name = connected_exchange.exchange.exchange_name
    # 거래소 이미지
    connected_exchange_image = "https://boida.s3.ap-northeast-2.amazonaws.com/{0}".format(
        connected_exchange.exchange.exchange_image)

    result = upbit_home(connected_exchange.access_key, connected_exchange.secret_key)

    # 업비트 거래소 연동되어 있으나, 데이터가 없을 경우
    if result.shape[0] == 0:
        response = {
            "user": {
                "user_name ": user_info.nickname,
                "user_profile": user_info.profile_image
            },
            "connected_exchange_total": {
                "valuation_amount": 0,
                "loss": 0,
                "earning_rate": 0,
            },
            "connected_exchange": [
                {
                    "connected_exchange_name": connected_exchange_name,
                    "connected_exchange_image": connected_exchange_image,
                    "valuation_amount": 0,
                    "loss": 0,
                    "earning_rate": 0,
                }
            ]

        }
        return Response(response, status=status.HTTP_200_OK)


    else:

        # 총 매수가(수익률 계산을 위해 필요함)
        purchase_amount = result["purchase_amount"].sum()

        # 총 평가액
        valuation_amount = result["valuation_amount"].sum()
        # 수익률
        earning_rate = (valuation_amount / purchase_amount) * 100 - 100
        # 평가손익
        loss = result["valuation_loss"].sum()

        response = {
            "user": {
                "user_name ": user_info.nickname,
                "user_profile": user_info.profile_image
            },
            "connected_exchange_total": {
                "valuation_amount": valuation_amount,
                "loss": loss,
                "earning_rate": earning_rate,
            },
            "connected_exchange": [
                {
                    "connected_exchange_name": connected_exchange_name,
                    "connected_exchange_image": connected_exchange_image,
                    "valuation_amount": valuation_amount,
                    "loss": loss,
                    "earning_rate": earning_rate,
                }
            ]

        }
        return Response(response, status=status.HTTP_200_OK)


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
