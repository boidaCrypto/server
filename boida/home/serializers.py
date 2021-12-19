from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, Asset, Transaction, ConnectedExchange


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    exchanges = ExchangeSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = (
            'exchanges', 'crypto', "purchase_amount", 'valuation_amount', 'valuation_loss',
            'valuation_earning_rate',
            'balance', 'crypto_ratio')


# 최근거래내역에 사용되는 시리얼라이저.
class ExchangeForTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ("id", "exchange_name", "exchange_image")


# 최근거래내역에 사용되는 시리얼라이저.
class ConnectedExchangeSerializer(serializers.ModelSerializer):
    # exchanges = ExchangeForTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = ConnectedExchange
        fields = ("id",)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['exchange'] = ExchangeForTransactionSerializer(instance.exchange).data
        return response
