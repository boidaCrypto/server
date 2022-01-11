import datetime

from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, ConnectedExchange, Transaction, ExchangeDescription


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('side', 'price', 'market', 'executed_volume', 'paid_fee', 'trades_count')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # market_name
        market_name = instance.market

        market_name_index = market_name.find('-')
        market = market_name[:market_name_index]

        # currency_name
        currency = market_name[market_name_index + 1:]

        # created_at, 2021-10-15 12:22:03과 같은 포맷으로 변경
        created_at = str(datetime.datetime.strptime(str(instance.created_at), "%Y-%m-%d %H:%M:%S"))

        # 체결금액
        executed_price = instance.price * instance.executed_volume

        # 체결금액 단위
        if market == 'BTC':
            executed_price_unit = "btc"
        else:
            executed_price_unit = "원"

        # 거래소 정보
        print(instance.connected_exchange.exchange)
        # Exchange.objects.get(id=)

        response["market_name"] = market
        response["currency_name"] = currency
        response["created_at"] = created_at
        response["executed_price"] = executed_price
        response["executed_price_unit"] = executed_price_unit

        response["exchange"] = {
            "exchange_name": instance.connected_exchange.exchange.exchange_name,
            "exchange_image": "https://boida.s3.ap-northeast-2.amazonaws.com/{0}".format(
                instance.connected_exchange.exchange.exchange_image)
        }

        return response
