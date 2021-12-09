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
from users.models import User
from sqlalchemy import create_engine
import pymysql
from exchange.models import Crypto, Asset


def accounts(access_key, secret_key):
    server_url = "https://api.upbit.com"

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    data = pd.json_normalize(res.json())
    data = data.astype({'balance': float, 'avg_buy_price': float, 'locked': float})
    return data


def get_coin_price(market_name):
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": market_name, "count": "1"}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    return res.json()


def get_btc_price():
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market": "KRW-BTC", "count": "1"}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    return res.json()[0]["trade_price"]


# Hoem API
def upbit_home(access_key, secret_key, user, exchange):

    data = accounts(access_key, secret_key)
    # 매수금액 평가금액, 평가손익, 평가수익률, 총보유자산
    container = pd.DataFrame(
        columns=['purchase_amount', 'valuation_amount', 'valuation_loss', 'valuation_earning_rate', 'crypto_id',
                 'balance'])

    # locked가 0이 아닌 행 가져오기.
    calculatable_coin = data[data.locked != 0]
    # locked가 아닌 행만 계산.
    for i in range(len(calculatable_coin)):
        a = calculatable_coin.loc[i + 1]

        ### 매수금액 계산
        purchase_amount = a.locked * a.avg_buy_price
        print("매수금액: {0}".format(purchase_amount))

        ### 평가금액 계산
        # 현재 해당 코인의 원화시세 가져오기
        coin_name = calculatable_coin["currency"][i+1]
        krw_market_name = "KRW-" + coin_name
        btc_market_name = "BTC-" + coin_name
        coin_price = get_coin_price(krw_market_name)
        if coin_price["error"]["name"] == 404:
            btc_krw_price = get_btc_price()
            coin_price = get_coin_price(btc_market_name)
            # 해당 코인 현재 원화가격 계산
            coin_price = coin_price[0]["trade_price"] * btc_krw_price
            # 최종 평가금액
            valuation_amount = coin_price * a.locked
            print("평가금액: {0}".format(valuation_amount))
        else:
            valuation_amount = coin_price[0]["trade_price"] * a.locked
            print("평가금액: {0}".format(valuation_amount))

        ### 평가손익 계산
        valuation_loss = valuation_amount - purchase_amount
        print("평가손익: {0}".format(valuation_loss))

        ### 평가수익률 계산
        valuation_earning_rate = (coin_price / a.avg_buy_price) * 100 - 100
        print("평가수익률: {0}".format(valuation_earning_rate))

        ### Crypto, 추후에 없을 경우 예외처리 진행.
        crypto = Crypto.objects.get(crypto_name=coin_name)

        # 최종적으로 테이블에 담기.
        container_row = {'crypto_id': crypto.id,
                         'purchase_amount': purchase_amount,
                         'valuation_amount': valuation_amount,
                         'valuation_loss': valuation_loss,
                         'valuation_earning_rate': valuation_earning_rate,
                         'balance': a.locked,
                         }

        container = container.append(container_row, ignore_index=True)

        # 기존의 upbit_asset 있을 경우 삭제
        upbit_asset = Asset.objects.filter(user=user)
        upbit_asset.delete()

        # 계산 결과 DB 저장
        container['user_id'] = user.id
        container['exchange_id'] = exchange.id

        # pymysql.install_as_MySQLdb()
        engine = create_engine(
            "mysql+mysqldb://admin:" + "admin1234" + "@boida.cpnbrmzhyf3q.ap-northeast-2.rds.amazonaws.com/boida",
            encoding='utf-8')
        conn = engine.connect()
        conn.execute("SET foreign_key_checks = 0;")
        container.to_sql(name='asset', con=conn, if_exists='append', index=False)
        conn.close()
