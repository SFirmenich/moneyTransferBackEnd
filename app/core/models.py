from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from coins.models import Coin
from django.db.models import Sum

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def balance_by_coin(self,coin):
        return self.movement_set.filter(coin=coin).aggregate(Sum('amount')).get("amount__sum") or 0

    def add_account_movement(self, amount, coin):
        Movement.objects.create(user=self, amount=amount, coin=coin)

class Movement(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=5)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    coin = models.ForeignKey(Coin, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.amount} {self.coin} - {self.user}"
