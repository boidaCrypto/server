from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'platform_type', 'platform_id', 'nickname','profile_image','thumbnail_image' )
