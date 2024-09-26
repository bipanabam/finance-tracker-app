from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Transaction
from .filters import TransactionFilter

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

def transaction_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related("category")
    )
    # print(transactions)
    context = {'filter': transaction_filter}
    if request.htmx:
        return render(request, 'tracker/partials/transaction-container.html', context)
    return render(request, 'tracker/transaction-list.html', context)