from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from transactions.tasks import process_transaction
from transactions.models import Transaction
from transactions.serializers import TransactionCreationSerializer, TransactionListSerializer
from itertools import chain

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        transaction = serializer.save()
        process_transaction.delay(transaction.id)

    def get_queryset(self):
        return Transaction.objects.filter(Q(origin=self.request.user)|Q(destiny=self.request.user)).order_by("-timestamp")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransactionListSerializer
        return TransactionCreationSerializer
