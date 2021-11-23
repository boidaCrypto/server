from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Test(request, format=None):

    return Response(status=status.HTTP_200_OK)