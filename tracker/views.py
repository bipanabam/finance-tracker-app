from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django_htmx.http import retarget

from .models import Transaction
from .filters import TransactionFilter

from .forms import TransactionForm

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

def transaction_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related("category")
    )
    # print(transactions)
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
               'filter': transaction_filter,
               'total_income': total_income,
               'total_expenses': total_expenses,
               'net_income': total_income - total_expenses,
               }
    if request.htmx:
        return render(request, 'tracker/partials/transaction-container.html', context)
    return render(request, 'tracker/transaction-list.html', context)

@login_required
def create_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': 'Transaction was added successfully!'}
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {'form': form}
            response = render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')
    context = {'form': TransactionForm}
    return render(request, 'tracker/partials/create-transaction.html', context)