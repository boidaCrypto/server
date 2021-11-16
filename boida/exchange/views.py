import pymysql
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange, Transaction
from exchange.serializers import APISerializer

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
    user_exchange = Exchange.objects.filter(user=user, is_deleted=False)
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



    # bulk_list = list()
    # for i in range(invoice_data.shape[0]):
    #     print(i)
    #     bulk_list.append(
    #         Upbit(
    #             exchange=exchange,
    #             uuid=invoice_data["uuid"][i],
    #             side=invoice_data["side"][i],
    #             ord_type=invoice_data["ord_type"][i],
    #             price=invoice_data["price"][i],
    #             state=invoice_data["state"][i],
    #             market=invoice_data["market"][i],
    #             volume=invoice_data["volume"][i],
    #             remaining_volume=invoice_data["remaining_volume"][i],
    #             reserved_fee=invoice_data["reserved_fee"][i],
    #             remaining_fee=invoice_data["remaining_fee"][i],
    #             paid_fee=invoice_data["paid_fee"][i],
    #             locked=invoice_data["locked"][i],
    #             executed_volume=invoice_data["executed_volume"][i],
    #             trades_count=invoice_data["trades_count"][i],
    #             created_at=invoice_data["created_at"][i]
    #         )
    #     )
    #
    # Upbit.objects.bulk_create(bulk_list)