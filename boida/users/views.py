from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import redirect
from django.conf import settings
from users.models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests as req
from rest_framework import status
from json.decoder import JSONDecodeError

CLIENT_ID = "415f1aec476684d25a44afce51a98d2f"
CLIENT_SECRET = "EIvtcyd8SreXsawSGZM3yBXrafJ8frO2"
KAKAO_CALLBACK_URI = "http://3.35.4.147:8000/users/kakao/callback/"
# KAKAO_CALLBACK_URI = "http://localhost:8000/users/kakao/callback/"
BASE_URL = 'http://localhost:8000/'


def kakao_login(request):
    # 카카오 로그인을 누르면, redirect된다.
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    # code를 받아서, access token을 제공받는다.
    code = request.GET.get("code")
    token_req = req.post(
        url="https://kauth.kakao.com/oauth/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": KAKAO_CALLBACK_URI,
            "code": code,
        },
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    # 제공받은 access token
    access_token = token_req_json.get("access_token")

    # 유저정보 얻기
    headers = ({'Authorization': f"Bearer {access_token}"})
    user_profile_info_uri = 'https://kapi.kakao.com/v2/user/me'
    user_profile_info = req.post(user_profile_info_uri, headers=headers)
    json_data = user_profile_info.json()
    print(json_data)
    print(json_data["id"])
    print(json_data["connected_at"])
    print(json_data["kakao_account"]["profile"]["nickname"])
    print(json_data["kakao_account"]["profile"]["thumbnail_image_url"])
    print(json_data["kakao_account"]["profile"]["profile_image_url"])
    print(json_data["kakao_account"]["email"])
    print(json_data["kakao_account"]["age_range"])
    print(json_data["kakao_account"]["gender"])


    data = {'access_token': access_token, 'code': code}
    print("data : ", data)
    print(BASE_URL,"users/kakao/login/finish/")
    accept = req.post(
        f"{BASE_URL}users/kakao/login/finish/", data=data)
    accept_status = accept.status_code
    if accept_status != 200:
        return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
    accept_json = accept.json()
    accept_json.pop('user', None)
    return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
