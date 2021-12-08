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