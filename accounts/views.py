from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Account, Transaction
from .forms import TransactionForm

def home(request):
    accounts = Account.objects.all()
    return render(request, 'home.html', {'accounts': accounts})

def account_detail(request, account_id):
    account = Account.objects.get(pk=account_id)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'account_detail.html', {'account': account, 'transactions': transactions})

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form})