from django.db import models
from coins.models import Coin
from core.models import Movement
from django.conf import settings

PENDING="PENDING"
APPROVED="APPROVED"
REJECTED="REJECTED"

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=5)

    TRANSACTION_STATES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    state = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATES,
        default=PENDING,
    )
    origin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="outcoming_transactions",
    )
    destiny = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incoming_transactions",
    )
    coin = models.ForeignKey(Coin, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.origin} -> {self.destiny} por {self.amount} {self.coin} | {self.state}"

    def process(self):
        if self.state == PENDING:
            if self.origin.balance_by_coin(self.coin) >= self.amount:
                self.origin.add_account_movement(self.amount*-1,self.coin)
                self.destiny.add_account_movement(self.amount,self.coin)
                self.state = APPROVED
            else:
                self.state = REJECTED
            self.save()
