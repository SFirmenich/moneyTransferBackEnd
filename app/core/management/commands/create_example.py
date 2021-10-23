import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from coins.models import Coin

class Command(BaseCommand):

    def handle(self,*args, **options):
        admin = get_user_model().objects.create_superuser('admin.user@challenge.com','password123')
        user1 = get_user_model().objects.create_user(email='simple.user@challenge.com',password="supersecret")
        user2 = get_user_model().objects.create_user(email='simple.user2@challenge.com',password="supersecret")
        dolar = Coin.objects.create(name="Dolar")
        bitcoin = Coin.objects.create(name="Bitcoin")
        pesos = Coin.objects.create(name="Peso")
        ethereum = Coin.objects.create(name="Ethereum")
        admin.add_account_movement(1000, dolar)
        admin.add_account_movement(10, bitcoin)
        admin.add_account_movement(50, ethereum)
        admin.add_account_movement(50000, pesos)
