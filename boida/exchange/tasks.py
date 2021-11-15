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

# 주문 리스트 조회 API
ORDER_LIST_API = "https://api.upbit.com/v1/orders"

def get_transaction(page_num, ACCESS_KEY, SECRET_KEY):
    query = {
        'state': 'done',  # 전체 체결 완료된 거래내역 수집
        'page': page_num
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
    res = requests.get(ORDER_LIST_API, query, headers=headers)

    data = res.json()
    if data == []:
        data = None
    return data

@shared_task
def exchange_synchronization(ACCESS_KEY, SECRET_KEY):
    print(ACCESS_KEY, SECRET_KEY)
    # 거래내역 데이터를 받아서, csv파일로 만든 뒤, DB에 저장.
    a = []
    for page_num in range(1, 100000000000000000):
        data = get_transaction(page_num, ACCESS_KEY, SECRET_KEY)
        # data가 없을경우 중지
        if data == None:
            break
        # json 스택
        a = a + data
    # 수집된 json 정보 dataframe화
    invoice_data = pd.json_normalize(a)
    print(invoice_data.shape)

    return None