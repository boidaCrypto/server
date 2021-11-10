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

rest_api_key = "415f1aec476684d25a44afce51a98d2f"
KAKAO_CALLBACK_URI = "http://localhost:8000/users/kakao/callback/"
BASE_URL = 'http://localhost:8000/'

def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")
    print("code-------------------------", code)
    redirect_uri = KAKAO_CALLBACK_URI
    token_req = req.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )

    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_req_json.get("access_token")
    print("access_token-------------------------", access_token)
    headers = ({'Authorization': f"Bearer {access_token}"})
    user_profile_info_uri = 'https://kapi.kakao.com/v2/user/me'
    user_profile_info = req.get(user_profile_info_uri, headers=headers)
    json_data = user_profile_info.json()
    print("json_data : ", json_data)

    data = {'access_token': access_token, 'code': code}
    accept = req.post(
        f"{BASE_URL}accounts/kakao/login/finish/", data=data)
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
