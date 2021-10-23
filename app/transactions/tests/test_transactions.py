from django.test import TestCase
from django.contrib.auth import get_user_model
from coins.models import Coin
from transactions.models import Transaction, PENDING, APPROVED, REJECTED
from core.models import Movement
from unittest.mock import patch


class TransactionTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user("name@challenge.com", 'password123')
        self.user2 = get_user_model().objects.create_user("name2@challenge.com", 'password123')
        self.bitcoin = Coin.objects.create(name="Bitcoin")

    def test_transaction_pending_at_creation(self):
        transaction = Transaction.objects.create(origin=self.user1,destiny=self.user2, amount=1, coin=self.bitcoin)
        self.assertEqual(transaction.state, PENDING)

    @patch('core.models.User.balance_by_coin', return_value=0)
    def test_transaction_process_get_rejected(self, balance_by_coin):
        transaction = Transaction.objects.create(origin=self.user1, destiny=self.user2, amount=1, coin=self.bitcoin)
        transaction.process()
        self.assertEqual(transaction.state, REJECTED)
        self.assertEqual(Movement.objects.count(), 0)

    @patch('core.models.User.balance_by_coin', return_value=1)
    def test_transaction_process_get_approved(self, balance_by_coin):
        transaction = Transaction.objects.create(origin=self.user1, destiny=self.user2, amount=1, coin=self.bitcoin)
        transaction.process()
        self.assertEqual(transaction.state, APPROVED)

    @patch('core.models.User.balance_by_coin')
    def test_transaction_process_get_approved_and_create_movements(self, balance_by_coin):
        balance_by_coin.return_value = 10
        transaction = Transaction.objects.create(origin=self.user1, destiny=self.user2, amount=1, coin=self.bitcoin)
        transaction.process()
        self.assertEqual(transaction.state, APPROVED)
        self.assertEqual(Movement.objects.count(), 2)
        origin_movement = Movement.objects.get(user=transaction.origin)
        destiny_movement = Movement.objects.get(user=transaction.destiny)
        self.assertEqual(origin_movement.amount, -1)
        self.assertEqual(destiny_movement.amount, 1)
