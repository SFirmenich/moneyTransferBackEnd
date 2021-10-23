from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import views
from rest_framework.response import Response
from user.serializers import UserSerializer, AuthTokenSerializer, BalanceSerializer
from django.shortcuts import get_object_or_404
from core.models import Coin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class BalanceByCoinView(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, coin_id):
        coin = get_object_or_404(Coin, id=coin_id)
        amount = request.user.balance_by_coin(coin)
        serializer = BalanceSerializer({"amount":amount, "coin":coin}, many=False)
        return Response(serializer.data)

class BalanceView(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        coins = Coin.objects.all()
        balance = []
        for coin in coins:
            balance.append({"amount":request.user.balance_by_coin(coin), "coin":coin})
        serializer = BalanceSerializer(balance, many=True)
        return Response(serializer.data)
