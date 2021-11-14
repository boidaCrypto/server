from rest_framework import serializers
from users.models import User
from exchange.models import exchange


class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = exchange
        fields = '__all__'
