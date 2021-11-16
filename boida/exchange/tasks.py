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

from users.models import User
from exchange.models import Exchange, Upbit

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
    user = User.objects.get(id=request_data.data["user"])
    exchange = Exchange.objects.create(user=user, exchange_type=request_data.data["exchange_type"],
                                       access_key=request_data.data["access_key"],
                                       secret_key=request_data.data["secret_key"])
    exchange.save()

    # 거래내역 데이터를 받아서, csv파일로 만든 뒤, DB에 저장.
    a = []
    for page_num in range(1, 100000000000000000):
        data = get_transaction(page_num, request_data.data["access_key"], request_data.data["secret_key"])
        if data == None:
            break
        a = a + data

    # 수집된 json 정보 dataframe화
    invoice_data = pd.json_normalize(a)
    exchange = Exchange.objects.get(user=user)
    invoice_data["exchange_id"] = exchange.id

    pymysql.install_as_MySQLdb()
    engine = create_engine(
        "mysql+mysqldb://admin:" + "admin1234" + "@boida.cpnbrmzhyf3q.ap-northeast-2.rds.amazonaws.com/boida",
        encoding='utf-8')
    conn = engine.connect()
    conn.execute("SET foreign_key_checks = 0;")
    invoice_data.to_sql(name='exchange_upbit', con=conn, if_exists='append', index=False)
    conn.close()

    return None
