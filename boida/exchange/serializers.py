from rest_framework import serializers
from users.models import User
from exchange.models import Exchange


class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'
