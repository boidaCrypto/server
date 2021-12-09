from rest_framework import serializers
from users.models import User
from exchange.models import Exchange, Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
