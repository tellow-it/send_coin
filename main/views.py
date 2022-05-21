from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
import requests
from .models import Transaction

# Create your views here.
from .send_transaction import Wallet, Coins, BCS_network


class TransactionViewList(ListView):
    model = Transaction
    context_object_name = 'list_tr'
    template_name = 'main/index.html'
    paginate_by = 5
    queryset = Transaction.objects.all()


class TransactionDetail(DetailView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'main/detail.html'


def send_transaction():
    wallet = Wallet()
    coin = Coins(int(1e8))
    network = BCS_network()
    network.create_transaction(wallet_for_tx=wallet, coin_for_tx=coin)
    transaction = network.signed_transaction_hex

    print('Transaction hex: ', transaction)

    send_raw_transaction = requests.post("http://bcs_tester:iLoveBCS@45.32.232.25:3669",
                                         json={'method': 'sendrawtransaction', 'params': [transaction]})

    return send_raw_transaction.json()['result']


def button_send_tx(request):
    if request.method == 'POST':
        result = send_transaction()
        tx = Transaction()
        tx.name = result
        tx.save()

    return redirect("list")
