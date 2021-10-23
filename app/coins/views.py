from coins.models import Coin
from coins.serializers import CoinSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CoinListCreate(generics.ListCreateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
