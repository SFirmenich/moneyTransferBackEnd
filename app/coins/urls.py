from django.urls import path
from .views import CoinListCreate

app_name = 'coins'
urlpatterns = [
    path('', CoinListCreate.as_view()),
]
