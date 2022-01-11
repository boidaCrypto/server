import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange, Transaction, Exchange, ExchangeDescription
from exchange.serializers import ConnectedExchangeSerializer, ExchangeSerializer, ListExchangeSerializer, \
    ListExchangeDescriptionSerializer

import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
from transaction.function import transaction_func


from exchange.tasks import exchange_synchronization
from firebase_admin import messaging


@api_view(['GET'])
@permission_classes([AllowAny])
def ConnectedExchangeList(requests, pk, format=None):
    user = User.objects.get(id=pk)
    user_exchange = ConnectedExchange.objects.filter(user=user, is_deleted=False)
    # 유저가 연결한 거래소가 없을 때
    if list(user_exchange) == []:
        print("hear")
        response = {
            "connected_exchange": []
        }
        return Response(response, status=status.HTTP_200_OK)
    # 유저가 연결한 거래소가 있을 때,
    else:
        connected_exchange = ConnectedExchangeSerializer(user_exchange, many=True)

        response = {
            "connected_exchange": connected_exchange.data
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def ListExchange(request, pk, format=None):
    # 현재 연동 가능한 국내 거래소 가져오기 + 사용자의 연결된 거래소인지 정보 추가하기
    domestic_exchange = Exchange.objects.filter(is_available=True, location="domestic")
    domestic_exchange = ListExchangeSerializer(domestic_exchange, many=True, context={"user": pk})

    # 현재 연동 가능한 해외 거래소 가져오기 + 사용자의 연결된 거래소인지 정보 추가하기
    aboard_exchange = Exchange.objects.filter(is_available=True, location="aboard")
    aboard_exchange = ListExchangeSerializer(aboard_exchange, many=True, context={"user": pk})

    data = {
        "domestic": domestic_exchange.data,
        "aboard": aboard_exchange.data
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def DeleteExchange(request, format=None):
    connected_exchange = ConnectedExchange.objects.get(user=request.data["user_id"],
                                                       pk=request.data["connected_exchange_id"])
    print(connected_exchange)
    connected_exchange.is_deleted = True
    connected_exchange.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def ConnectingExchange(request, format=None):
    print("Access_key : ", request.data["access_key"])
    print("SECRET_KEY : ", request.data["secret_key"])
    # API KEY 이상 결과 전달.
    test = api_test(request.data["access_key"], request.data["secret_key"])
    if test == 401:
        data = {
            "msg": "wrong API key",
            "exchange_throw_status": "403"
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    # # 유저의 거래내역 연동을 위한 비동기 처리 파트
    exchange_synchronization.delay(request.data)

    data = {
        "msg": "correct API key",
        "exchange_throw_status": test
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def CheckExchangeSynchronized(request, format=None):
    user = request.data['user_id']
    exchange = request.data['exchange_id']
    connected_exchange = ConnectedExchange.objects.filter(user=user, exchange=exchange, is_sync=True)

    if list(connected_exchange) == []:
        # 204이면, 연결된 거래소가 없음을 나타냄.
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        # 200이면, 연결된 거래소가 존재
        return Response(status=status.HTTP_200_OK)


def api_test(ACCESS_KEY, SECRET_KEY):
    print("Access_key : ", ACCESS_KEY)
    print("SECRET_KEY : ", SECRET_KEY)

    test = "https://api.upbit.com/v1/orders"
    query = {
        'state': 'done',
        'page': 1
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, SECRET_KEY)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(test, query, headers=headers)
    return res.status_code


@api_view(['GET'])
@permission_classes([AllowAny])
def ListExchangeDescription(request, pk, format=None):
    exchange_description = ExchangeDescription.objects.filter(exchange=pk).order_by("id")
    exchange_description = ListExchangeDescriptionSerializer(exchange_description, many=True)
    data = {
        "exchange_description": exchange_description.data
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def FirebaseTest(request, format=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title='{0}와 연동이 완료되었습니다.'.format("upbit"),
            body='{0}와 연동이 완료되었습니다.'.format("upbit")
        ),
        token="fAghHDLdRvyltpmDB3itF0:APA91bHvKHyUW3f1xYFv8wmJYxICrssbdOWMxml6XHBtGFcsDgqN26Cq7RbZKQUnGZnK8Id185_z-4fYrHgeVldCyXbdTfZTEJSD7PlrgQzIk6vu-xPf_eZ5fV0sEsS8RbB6eEpJ8kj1",
    )
    response = messaging.send(message)
    print("Successfully sent message", response)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def ListExchangeAsset(request, format=None):
    # 상단파트(그래프 등등)

    # 상세 자산 파트

    # 최근 거래내역 파트
    connected_exchange = ConnectedExchange.objects.get(user=request.data["user_id"], exchange=1)
    transaction = Transaction.objects.filter(connected_exchange=connected_exchange).order_by("-created_at")[:5]

    result = transaction_func(transaction)
    # price : 체결가격, executed_volume : 체결수량, executed_price : 체결가격,


    response = {
        # 상단 파트의 결과

        # 상세 자산 파트의 결과


        # 최근 거래내역 파트의 결과
        "connected_exchange": result[0],
        "transaction": result[1]
    }

    return Response(response, status=status.HTTP_200_OK)
