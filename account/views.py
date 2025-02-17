from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm
from .models import Account
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import os

# Create an Account
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        
        if form.is_valid():
            account = form.save(commit=False)
            account.status = request.POST.get('status') == 'on'
            account.save()
            
            messages.success(request, 'Account created successfully.')
            return redirect('list_account')
        else:
            messages.error(request, 'Error creating account. Please try again.')
    else:
        form = AccountForm()
    
    parent_accounts = Account.objects.filter(parent__isnull=True, status=True)

    context = {
        'link': 'create_account',
        'form': form,
        'parent_accounts': parent_accounts,
    }
        
    return render(request, 'backend/account/create_account.html', context)

# List Accounts with Pagination
def list_account(request):
    accounts = Account.objects.order_by('-id')
    paginator = Paginator(accounts, 10)
    page = request.GET.get('page')
    accounts = paginator.get_page(page)

    context = {
        'accounts': accounts,
        'link': 'list_account'
    }

    return render(request, 'backend/account/list_account.html', context)

# Edit an Account
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account.status = request.POST.get('status') == 'on'
            form.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('list_account')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccountForm(instance=account)

    parent_accounts = (
        Account.objects.none() if Account.objects.filter(parent=account).exists()
        else Account.objects.filter(parent__isnull=True, status=True).exclude(id=account.id)
    )

    context = {
        'form': form,
        'account': account,
        'parent_accounts': parent_accounts,
    }

    return render(request, 'backend/account/edit_account.html', context)

# Delete an Account (AJAX)
@require_POST
def delete_account(request, pk):
    try:
        data = get_object_or_404(Account, pk=pk)
        data.delete()
        messages.info(request, 'Account deleted successfully.')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
