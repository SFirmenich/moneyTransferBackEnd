from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from transactions.models import Transaction
import time

class TransactionCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('destiny','coin','amount')

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError({"amount":"Transaction's amount must be greater than 0."})
        return data

    def create(self, validated_data):
        origin = request=self.context.get('request').user
        validated_data["origin"] = origin
        transaction = super().create(validated_data)
        return transaction

class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

class TransactionListSerializer(serializers.ModelSerializer):
    coin = serializers.SerializerMethodField()
    timestamp = TimestampField()

    class Meta:
        model = Transaction
        fields = ('origin','destiny','coin','amount','timestamp', 'state')

    def get_coin(self, obj):
        return obj.coin.name
