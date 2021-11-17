import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange, Transaction, Exchange
from exchange.serializers import ConnectedExchangeSerializer, ExchangeSerializer, ListExchangeSerializer

import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import csv
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb

from exchange.tasks import exchange_synchronization


@api_view(['GET'])
@permission_classes([AllowAny])
def ConnectedExchangeList(requests, pk, format=None):
    user = User.objects.get(id=pk)
    user_exchange = ConnectedExchange.objects.filter(user=user, is_deleted=False)
    # 유저가 연결한 거래소가 없을 때
    if list(user_exchange) == []:
        user_exchange_info = []
        return Response(user_exchange_info, status=status.HTTP_204_NO_CONTENT)
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
def ConnectingExchange(request, format=None):
    # API KEY 이상 결과 전달.
    test = api_test(request.data["access_key"], request.data["secret_key"])
    if test == 401:
        data = {
            "msg": "wrong API key",
            "exchange_throw_status": "401"
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    # # 유저의 거래내역 연동을 위한 비동기 처리 파트
    exchange_synchronization.delay(request.data)

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

# def get_transaction(page_num, access_key, secret_key):
#     ORDER_LIST_API = "https://api.upbit.com/v1/orders"
#     query = {
#         'state': 'done',  # 전체 체결 완료된 거래내역 수집
#         'page': page_num
#     }
#     query_string = urlencode(query).encode()
#
#     m = hashlib.sha512()
#     m.update(query_string)
#     query_hash = m.hexdigest()
#
#     payload = {
#         'access_key': access_key,
#         'nonce': str(uuid.uuid4()),
#         'query_hash': query_hash,
#         'query_hash_alg': 'SHA512',
#     }
#
#     jwt_token = jwt.encode(payload, secret_key)
#     authorize_token = 'Bearer {}'.format(jwt_token)
#     headers = {"Authorization": authorize_token}
#     res = requests.get(ORDER_LIST_API, query, headers=headers)
#
#     data = res.json()
#     if data == []:
#         data = None
#     return data


# # -----------------------------------------------------------------
#
# user = User.objects.get(id=request.data["user"])
# exchange = Exchange.objects.get(exchange_type=request.data["exchange_type"])
# print(user, "user-------------------")
# connect_exchange = ConnectedExchange.objects.create(user=user, exchange=exchange,
#                                                     access_key=request.data["access_key"],
#                                                     secret_key=request.data["secret_key"])
# connect_exchange.save()
#
# # 거래내역 데이터를 받아서, csv파일로 만든 뒤, DB에 저장.
# a = []
# for page_num in range(1, 100000000000000000):
#     data = get_transaction(page_num, request.data["access_key"], request.data["secret_key"])
#     if data == None:
#         break
#     a = a + data
#
# # 수집된 json 정보 dataframe화
# invoice_data = pd.json_normalize(a)
# connected_exchange = ConnectedExchange.objects.get(user=user)
# invoice_data["connected_exchange_id"] = connected_exchange.id
#
# pymysql.install_as_MySQLdb()
# engine = create_engine(
#     "mysql+mysqldb://admin:" + "admin1234" + "@boida.cpnbrmzhyf3q.ap-northeast-2.rds.amazonaws.com/boida",
#     encoding='utf-8')
# conn = engine.connect()
# conn.execute("SET foreign_key_checks = 0;")
# invoice_data.to_sql(name='transaction', con=conn, if_exists='append', index=False)
# conn.close()
#
# # -----------------------------------------------------------------
