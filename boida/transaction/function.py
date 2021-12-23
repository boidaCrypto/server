from exchange.models import ConnectedExchange
from home.serializers import ConnectedExchangeSerializer
import pandas as pd

def transaction_func(transaction):
    # 일자별로 분류하기
    transaction = pd.DataFrame(
        transaction.values("id", "connected_exchange_id", "side", "price", "market", "executed_volume",
                           "created_at"))
    # year-month-day
    ymd = transaction["created_at"].dt.strftime("%Y-%m-%d")
    # hour-minute
    hm = transaction["created_at"].dt.strftime("%H:%M")
    transaction["ymd"] = ymd
    transaction["hm"] = hm
    # 얼마 샀는지
    transaction["executed_price"] = transaction["price"] * transaction["executed_volume"]

    # 날짜 중복 제거
    common_created_at = ymd.drop_duplicates(keep='first')
    result = []
    for i in common_created_at:
        data1 = transaction[transaction["ymd"] == i].to_dict(orient='records')
        data2 = {"date": i, "data": data1}
        result.append(data2)

    # 거래소 정보 가져오기.
    exchange_id = transaction["connected_exchange_id"].drop_duplicates(keep='first').values
    connected_exchange = ConnectedExchange.objects.filter(id__in=exchange_id, is_deleted=False)
    connected_exchange = ConnectedExchangeSerializer(connected_exchange, many=True).data
    return [connected_exchange, result]
