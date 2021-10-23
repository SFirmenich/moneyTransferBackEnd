from django.urls import path
from .views import TransactionListCreate

app_name = 'transactions'
urlpatterns = [
    path('', TransactionListCreate.as_view(), name='transactions'),
]
