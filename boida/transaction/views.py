from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.models import User
from exchange.models import ConnectedExchange
from exchange.models import Transaction
from transaction.serializers import TransactionSerializer
from transaction.function import transaction_func


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Test(request, format=None):
    # 현재 활동중인 User를 가져온다.
    now_active_user = User.objects.filter(now_active=True)
    print(now_active_user)
    # 활동중이면서, UPBIT 거래소를 연동한
    # User.objects.extra(tables=['connected_exchange'], where=[''])
    print(now_active_user.objects.extra(tables=['connected_exchange'], where=['exchange_id=1']))

    return Response(status=status.HTTP_200_OK)


PAGE_SIZE = 10


@api_view(['POST'])
@permission_classes([AllowAny])
def ToalTransactionList(request, page, format=None):
    # 거래내역은 django orm을 사용하지 않아 직접 로직개발을 해야한다.,
    # 중간에 데이터가 추가되었을 떄도, 유지가 되고 불러와져야 한다.
    page = page
    user = request.data["user_id"]
    connected_exchange = ConnectedExchange.objects.get(user=user, exchange=1)
    # Count 내부 동작 성능, https://velog.io/@dev_dolxegod/Django-%EC%95%8C%EA%B3%A0-%EC%82%AC%EC%9A%A9%ED%95%98%EC%9E%90-Queryset-%EC%B9%B4%EC%9A%B4%ED%8A%B8-%EB%82%B4%EB%B6%80-%EB%8F%99%EC%9E%91
    transaction_cnt = Transaction.objects.filter(connected_exchange=connected_exchange).count()

    # 처음 페이지
    if page == 1:
        start_num = 1
        end_num = start_num * PAGE_SIZE

        # 여기서부터 데이터 포맷 변경하면 됨.
        transaction = Transaction.objects.filter(connected_exchange=connected_exchange).order_by("-created_at")[
                      start_num:end_num]
        result = transaction_func(transaction)

        # 결과
        next = "http://127.0.0.1:8000/transaction/total-transaction-list/{0}".format(page + 1)
        previous = None

        response = {
            "next": next,
            "previous": previous,
            "connected_exchange": result[0],
            "transaction": result[1]
        }
        return Response(response, status=status.HTTP_200_OK)

    # 전체 거래내역 개수가 페이지* 페이지 사이즈보다 작을 떄,
    elif transaction_cnt < (page * PAGE_SIZE):
        end_num = transaction_cnt
        start_num = end_num - PAGE_SIZE

        # 여기서부터 데이터 포맷 변경하면 됨.
        transaction = Transaction.objects.filter(connected_exchange=connected_exchange).order_by("-created_at")[
                      start_num:end_num]
        result = transaction_func(transaction)

        # 결과
        next = "http://127.0.0.1:8000/transaction/total-transaction-list/{0}".format(page + 1)
        previous = "http://127.0.0.1:8000/transaction/total-transaction-list/{0}".format(page - 1)

        response = {
            "next": next,
            "previous": previous,
            "connected_exchange": result[0],
            "transaction": result[1]
        }
        return Response(response, status=status.HTTP_200_OK)

    else:
        end_num = page * PAGE_SIZE
        start_num = end_num - PAGE_SIZE

        # 여기서부터 데이터 포맷 변경하면 됨.
        transaction = Transaction.objects.filter(connected_exchange=connected_exchange).order_by("-created_at")[
                      start_num:end_num]
        result = transaction_func(transaction)

        # 결과
        next = "http://127.0.0.1:8000/transaction/total-transaction-list/{0}".format(page + 1)
        previous = "http://127.0.0.1:8000/transaction/total-transaction-list/{0}".format(page - 1)

        response = {
            "next": next,
            "previous": previous,
            "connected_exchange": result[0],
            "transaction": result[1]
        }
        return Response(response, status=status.HTTP_200_OK)
