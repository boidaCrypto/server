from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from users.models import User
from exchange.models import exchange
from exchange.serializers import APISerializer

import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests


@api_view(['GET'])
@permission_classes([AllowAny])
def ConnectedExchangeList(requests, pk, format=None):
    user = User.objects.get(id=pk)
    user_exchange = exchange.objects.filter(user=user, is_deleted=False)
    # 유저가 연결한 거래소가 없을 때
    if list(user_exchange) == []:
        user_exchange_info = []
        return Response(user_exchange_info, status=status.HTTP_204_NO_CONTENT)
    # 유저가 연결한 거래소가 있을 때(추후 개발)
    else:
        user_exchange_info = {
            "성공": "성공"
        }
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def ConnectingExchange(requests, format=None):
    # API KEY 이상 결과 전달.
    test = api_test(requests.data["api_key"], requests.data["secret_key"])
    if test == 401:
        data = {
            "msg": "wrong API key",
            "exchange_throw_status": "401"
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    # API에 이상이없으면, 동기화 진행(현재는 정적으로 데이터 동기화 진행하고, 추후 비동기처리 진행하기.)

    data = {
        "msg": "correct API key",
        "exchange_throw_status": test
    }
    return Response(data, status=status.HTTP_200_OK)


def api_test(ACCESS_KEY, SECRET_KEY):
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
