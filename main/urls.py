from django.urls import path

from . import views
from .views import TransactionViewList
from .views import TransactionDetail

urlpatterns = [
    path('', TransactionViewList.as_view(), name='list'),
    path('tx/<int:pk>', TransactionDetail.as_view(), name='detail'),
    path('send/', views.button_send_tx, name='button_send'),
]