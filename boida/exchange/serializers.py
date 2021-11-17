from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, ConnectedExchange, Transaction


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class ConnectedExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedExchange
        fields = ('id', 'exchange')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['exchange'] = ExchangeSerializer(instance.exchange).data
        return response


class ListExchangeSerializer(serializers.ModelSerializer):
    is_connected = serializers.BooleanField(required=False)

    class Meta:
        model = Exchange
        fields = ('id', 'exchange_name', 'exchange_image', "is_connected")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        user = self.context.get("user")
        connected_exchange = ConnectedExchange.objects.filter(user=user, exchange=instance)
        if list(connected_exchange) == []:
            response["is_connected"] = False
        else:
            response["is_connected"] = True

        return response
