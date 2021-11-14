from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import redirect
from django.conf import settings
from users.models import User
from users.serializers import UserSerializer
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests as req
from rest_framework import status
from json.decoder import JSONDecodeError
from users.models import User

CLIENT_ID = "415f1aec476684d25a44afce51a98d2f"
CLIENT_SECRET = "EIvtcyd8SreXsawSGZM3yBXrafJ8frO2"
# KAKAO_CALLBACK_URI = "http://3.35.4.147:8000/users/kakao/callback/"
KAKAO_CALLBACK_URI = "http://localhost:8000/users/kakao/callback/"
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
            # "client_secret": CLIENT_SECRET,
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
    kakao_user = user_profile_info.json()

    # 해당 이메일로 가입한 유저가 있는지 확인, 추후 get_or_create로 가능한지 확인.
    try:
        user = User.objects.get(email=kakao_user["kakao_account"]["email"])
    except User.DoesNotExist:
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
            # access_token=accept_json["access_token"],
            # refresh_token=accept_json["refresh_token"],
        )
        user_create.save()
        return JsonResponse({"msg": "201 회원가입 완료되었습니다."}, status=status.HTTP_201_CREATED)

    # 회원이 이미 존재하면 회원정보 담아서 보내주기.
    user_info = UserSerializer(user)
    data = {
        "msg": "200 이미 가입된 회원입니다.",
        "user" : user_info.data
    }
    return JsonResponse(data, status=status.HTTP_201_CREATED)


class KakaoLogin(SocialLoginView):
    print("호출완료")
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI



    # data = {'access_token': access_token, 'code': code}
    # print("data : ", data)
    # print(BASE_URL, "users/kakao/login/finish/")
    # accept = req.post(
    #     f"{BASE_URL}users/kakao/login/finish/", data=data)
    # accept_status = accept.status_code
    # print("accept_status : ", accept_status)
    # if accept_status != 200:
    #     return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
    # accept_json = accept.json()
    # accept_json.pop('user', None)
    #
    # return JsonResponse(accept_json)
