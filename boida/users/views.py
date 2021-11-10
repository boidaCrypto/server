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
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError

rest_api_key = "415f1aec476684d25a44afce51a98d2f"
KAKAO_CALLBACK_URI = "http://localhost:8000/users/kakao/callback"


@api_view(['POST'])
@permission_classes([AllowAny])
def LocalRegister(request, format=None):
    kakao_authorization_code = request.data["kakao_authorization_code"]
    redirect_uri = request.data["redirect_uri"]
    return Response({"kakao_authorization_code": kakao_authorization_code, "redirect_uri" : redirect_uri}, status=status.HTTP_200_OK)


def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


# def kakao_callback(request):
#     rest_api_key = "415f1aec476684d25a44afce51a98d2f"
#     code = request.GET.get("code")
#     redirect_uri = KAKAO_CALLBACK_URI
#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
#     )
#
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#
#     access_token = token_req_json.get("access_token")
#
#     profile_request = requests.get(
#         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}
#     )
#     profile_json = profile_request.json()
#     kakao_account = profile_json.get('kakao_account')
#     email = kakao_account.get('email')
#     try:
#         user = User.objects.get(email=email)
#         social_user = SocialAccount.objects.get(user=user)
#         if social_user is None:
#             return JsonResponse({'err_msg'})
