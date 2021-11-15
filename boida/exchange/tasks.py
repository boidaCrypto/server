from celery import shared_task

import pandas
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import csv
import pandas as pd
import json
from time import sleep
import numpy as np
from sqlalchemy import create_engine
import pymysql
import MySQLdb

from exchange.models import Upbit, Exchange
from users.models import User

# 주문 리스트 조회 API
ORDER_LIST_API = "https://api.upbit.com/v1/orders"


def get_transaction(page_num, access_key, secret_key):
    query = {
        'state': 'done',  # 전체 체결 완료된 거래내역 수집
        'page': page_num
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(ORDER_LIST_API, query, headers=headers)

    data = res.json()
    if data == []:
        data = None
    return data


@shared_task
def exchange_synchronization(request_data):
    #  Access_key, secret_key 저장
    print(request_data['user'])
    user = User.objects.get(id=request_data["user"])
    user = Exchange.objects.create(user=user, exchange_type=request_data["exchange_type"],
                                   access_key=request_data["access_key"],
                                   secret_key=request_data["secret_key"])
    exchange = user.save()

    # 거래내역 데이터를 받아서, csv파일로 만든 뒤, DB에 저장.
    a = []
    for page_num in range(1, 100000000000000000):
        data = get_transaction(page_num, request_data["access_key"], request_data["secret_key"])
        # data가 없을경우 중지
        if data == None:
            break
        # json 스택
        a = a + data
    # 수집된 json 정보 dataframe화
    invoice_data = pd.json_normalize(a)

    # DB 저장
    Upbit.objects.bulk_create(exchange=exchange,
                              uuid=invoice_data["uuid"],
                              side=invoice_data["side"],
                              ord_type=invoice_data["ord_type"],
                              price=invoice_data["price"],
                              state=invoice_data["state"],
                              market=invoice_data["market"],
                              volume=invoice_data["volume"],
                              remaining_volume=invoice_data["remaining_volume"],
                              reserved_fee=invoice_data["reserved_fee"],
                              remaining_fee=invoice_data["remaining_fee"],
                              paid_fee=invoice_data["paid_fee"],
                              locked=invoice_data["locked"],
                              executed_volume=invoice_data["executed_volume"],
                              trades_count=invoice_data["trades_count"],
                              created_at=invoice_data["created_at"]
                              )

    return None
