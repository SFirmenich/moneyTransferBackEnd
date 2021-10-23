from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Movement
from coins.models import Coin

class UserBalanceTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("name@challenge.com", 'password123')
        self.dolar = Coin.objects.create(name="Dolar")
        self.bitcoin = Coin.objects.create(name="Bitcoin")
        Movement.objects.create(amount=1, user=self.user, coin=self.bitcoin)

    def test_movements_in_other_coins(self):
        bitcoin_balance = self.user.balance_by_coin(self.bitcoin)
        self.assertEqual(bitcoin_balance, 1)
        Movement.objects.create(amount=10, user=self.user, coin=self.dolar)
        bitcoin_balance = self.user.balance_by_coin(self.bitcoin)
        self.assertEqual(bitcoin_balance, 1)

    def test_outcoming_movements(self):
        bitcoin_balance = self.user.balance_by_coin(self.bitcoin)
        self.assertEqual(bitcoin_balance, 1)
        Movement.objects.create(amount=-1, user=self.user, coin=self.bitcoin)
        bitcoin_balance = self.user.balance_by_coin(self.bitcoin)
        self.assertEqual(bitcoin_balance, 0)

    def test_incoming_movements(self):
        bitcoin_balance = self.user.balance_by_coin(self.bitcoin)
        self.assertEqual(bitcoin_balance, 1)
        Movement.objects.create(amount=3, user=self.user, coin=self.bitcoin)
        bitcoin_balance = self.user.balance_by_coin(self.bitcoin)
        self.assertEqual(bitcoin_balance, 4)

    def test_add_account_movement(self):
        user = get_user_model().objects.create_user("username@challenge.com", 'password123')
        user.add_account_movement(amount=100,coin=self.dolar)
        self.assertEqual(user.movement_set.count(),1)
        user.add_account_movement(amount=100,coin=self.bitcoin)
        self.assertEqual(user.movement_set.count(),2)
