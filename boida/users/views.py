import requests
from django.contrib.auth.hashers import make_password, check_password
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from django.shortcuts import redirect
from django.conf import settings
from users.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.serializers import UserSerializer
import requests as req
from rest_framework import status

from users.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

# CLIENT_ID = "415f1aec476684d25a44afce51a98d2f"
CLIENT_ID = "31f8b74ba4ecfca1ff788f63b8a57c80"
CLIENT_SECRET = "EIvtcyd8SreXsawSGZM3yBXrafJ8frO2"
KAKAO_CALLBACK_URI = "http://3.35.4.147:8000/users/kakao/callback/"
# KAKAO_CALLBACK_URI = "http://localhost:8000/users/kakao/callback/"
BASE_URL = 'http://localhost:8000/'

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_login(request, format=None):
    access_token = request.data["access_token"]
    refresh_token = request.data["refresh_token"]
    fcm_token = request.data["fcm_token"]

    # 유저정보 얻기
    headers = ({'Authorization': f"Bearer {access_token}"})
    user_profile_info_uri = 'https://kapi.kakao.com/v2/user/me'
    user_profile_info = req.post(user_profile_info_uri, headers=headers)
    kakao_user = user_profile_info.json()
    try:
        user = User.objects.get(email=kakao_user["kakao_account"]["email"])
    except User.DoesNotExist:
        # access token 발급받는 로직 저장 후, create에 넣어준다.
        print("회원가입된 이메일이 없어 회원가입을 진행합니다.")
        user_create = User.objects.create(
            email=kakao_user["kakao_account"]["email"],
            platform_type="kakao",
            platform_id=kakao_user["id"],
            nickname=kakao_user["kakao_account"]["profile"]["nickname"],
            age_range=kakao_user["kakao_account"]["age_range"],
            gender=kakao_user["kakao_account"]["gender"],
            profile_image=kakao_user["kakao_account"]["profile"]["profile_image_url"],
            thumbnail_image=kakao_user["kakao_account"]["profile"]["thumbnail_image_url"],
            fcm_token=fcm_token
        )
        user_create.save()
        user = User.objects.get(email=kakao_user["kakao_account"]["email"])

        # access token, refresh token 생성, 유저가 가입되어(db에 존재) 있어야만 발급받을 수 있다.
        refresh = RefreshToken.for_user(user)
        user = UserSerializer(user)

        print(str(refresh), str(refresh.access_token), "000000000000000000000000000000000000")

        data = {
            "msg": "가입되었습니다.",
            "user": user.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(data, status=status.HTTP_201_CREATED)

    # 회원이 이미 존재하면 회원정보 담아서 보내주기.
    refresh = RefreshToken.for_user(user)
    user_info = UserSerializer(user)
    data = {
        "msg": "200 이미 가입된 회원입니다.",
        "user": user_info.data,
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def TestToken(request, format=None):

    user = User.objects.get(email=request.data["email"])

    # access token, refresh token 생성, 유저가 가입되어(db에 존재) 있어야만 발급받을 수 있다.
    refresh = RefreshToken.for_user(user)

    data = {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
    return Response(data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

@api_view(['POST'])
@permission_classes([AllowAny])
def IsActive(request, format=None):
    user = User.objects.get(id=request.data["user_id"])
    user.now_active = request.data["now_active"]
    user.save()
    return Response(status=status.HTTP_200_OK)