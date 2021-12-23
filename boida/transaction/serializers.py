from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, ConnectedExchange, Transaction, ExchangeDescription


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
