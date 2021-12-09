from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, Asset


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
