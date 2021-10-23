from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from coins.models import Coin

TRANSACTIONS_URL = reverse('transactions:transactions')

def create_user(**param):
    return

class PublicTransactionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_transactions_list_not_accessible(self):
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_transactions_create_not_accessible(self):
        payload = {
            'origin':'1',
            'coin':'1',
            'amount':'10'
        }
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserAPITest(TestCase):
    def setUp(self):
        self.login_user = get_user_model().objects.create_user(email='user@app.com', password='password123')
        self.destiny_user = get_user_model().objects.create_user(email='user2@app.com', password='password123')
        self.dolar = Coin.objects.create(name="Dolar")
        self.login_user.add_account_movement(amount=1000, coin=self.dolar)
        self.client = APIClient()
        self.client.force_authenticate(user=self.login_user)

    def test_transactions_create(self):
        payload = {
            'destiny': self.destiny_user.id,
            'coin':self.dolar.id,
            'amount':'10'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_transactions_create_non_existent_coin(self):
        payload = {
            'destiny': self.destiny_user.id,
            'coin':self.dolar.id+1,
            'amount':'10'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transactions_create_non_existent_destiny(self):
        payload = {
            'destiny': self.destiny_user.id+1,
            'coin':self.dolar.id,
            'amount':'10'
        }
        res = self.client.post(TRANSACTIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
