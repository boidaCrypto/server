from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, ConnectedExchange, Transaction, ExchangeDescription


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['exchange_color'] = int(instance.exchange_color, 16)
    #     return response



class ConnectedExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedExchange
        fields = ('id', 'exchange', )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['exchange'] = ExchangeSerializer(instance.exchange).data
        return response


class ListExchangeSerializer(serializers.ModelSerializer):
    is_connected = serializers.BooleanField(required=False)

    class Meta:
        model = Exchange
        fields = ('id', 'exchange_name', 'exchange_image', 'exchange_color', "has_qr", "is_connected")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        user = self.context.get("user")
        connected_exchange = ConnectedExchange.objects.filter(user=user, exchange=instance, is_deleted=False)
        if list(connected_exchange) == []:
            response["is_connected"] = False
        else:
            response["is_connected"] = True

        return response


class ListExchangeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeDescription
        fields = ('id', 'description', 'image')
