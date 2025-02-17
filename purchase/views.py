from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction 
from .forms import PurchaseForm
from .models import Purchase
from transaction.models import Transaction
from supplier.models import Supplier
from product.models import ProductVariant
from account.models import Account
from journalentry.models import JournalEntry 
from stock.models import StockMovement 
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Ensures all inserts happen together
                    # Create a transaction record
                    transaction_record = Transaction.objects.create()

                    # Create purchase and link it to the transaction
                    purchase = form.save(commit=False)
                    purchase.transaction = transaction_record
                    purchase.save()

                    # Get payment method & related account
                    paid_by = request.POST.get("paid_by")  # 'cash', 'bank', or 'accountpayable'
                    total_amount = purchase.total_amount

                    debit_account = Account.objects.get(slug="purchase")  # Debit account
                    credit_account = None

                    if paid_by == "cash":
                        credit_account = Account.objects.get(slug="cash")
                    elif paid_by == "bank":
                        credit_account = Account.objects.get(slug="bank")
                    elif paid_by == "accountpayable":
                        credit_account = Account.objects.get(slug="accountpayable")

                    if not credit_account:
                        raise ValueError("Invalid payment method selected.")

                    # Insert Double-Entry Journal Entries with unique transaction IDs
                    journal_entries = [
                        JournalEntry(transaction=transaction_record, account=debit_account, entry_type="debit", amount=total_amount, date=purchase.date),
                        JournalEntry(transaction=transaction_record, account=credit_account, entry_type="credit", amount=total_amount, date=purchase.date),
                    ]

                    # Use bulk_create to insert multiple entries
                    JournalEntry.objects.bulk_create(journal_entries)

                    # Update stock movements
                    products = request.POST.getlist('products[]')
                    prices = request.POST.getlist('prices[]')
                    quantities = request.POST.getlist('quantities[]')

                    for product_id, price, qty in zip(products, prices, quantities):
                        product_variant = ProductVariant.objects.get(id=product_id)
                        StockMovement.objects.create(
                            transaction=transaction_record,
                            account_name=debit_account,  # Assuming acts as an account
                            product_variant=product_variant,
                            movement_type="IN",
                            quantity=int(qty),
                            amount=float(price), 
                        )

                    messages.success(request, 'Purchase created successfully!')
                    return redirect('list_purchase')

            except Exception as e:
                messages.error(request, f"Error creating purchase: {str(e)}")

        else:
            messages.error(request, 'Error creating purchase. Please check the form and try again.')

    else:
        form = PurchaseForm()

    context = {
        'form': form,
        'suppliers': Supplier.objects.all(),
        'variants': ProductVariant.objects.all(),
    }

    return render(request, 'backend/purchase/create_purchase.html', context)

def list_purchase(request):
    purchases = Purchase.objects.all().order_by('-date')  # Fetch all purchases sorted by date
    paginator = Paginator(purchases, 10)  # Paginate with 10 purchases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'purchases': page_obj
    }
    return render(request, 'backend/purchase/list_purchase.html', context)


def view_purchase(request, purchase_id):
    # Fetch the purchase details
    purchase = get_object_or_404(Purchase, id=purchase_id)
    credit_entry = JournalEntry.objects.filter(transaction=purchase.transaction, entry_type="credit").first()
    # Fetch the stock movements related to this purchase
    recorded_variants = StockMovement.objects.filter(transaction=purchase.transaction)

    context = {
        'purchase': purchase,
        'credit_entry': credit_entry,
        'recorded_variants': recorded_variants,
    }

    return render(request, 'backend/purchase/view_purchase.html', context)

def edit_purchase(request, id):
    # Fetch the existing purchase
    purchase = get_object_or_404(Purchase, id=id)
    credit_entry = JournalEntry.objects.filter(transaction=purchase.transaction, entry_type="credit").first()
    # Access the transaction record related to the purchase
    transaction_record = purchase.transaction  # Assuming Purchase model has a ForeignKey to Transaction

    # Fetch the variants associated with the stock movements in the current transaction
    recorded_variants = StockMovement.objects.filter(transaction=transaction_record)

    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        
        if form.is_valid():
            try:
                with transaction.atomic():  # Ensures all updates happen together
                    # Get payment method & related account
                    paid_by = request.POST.get("paid_by")
                    total_amount = purchase.total_amount
                    
                    # Handle Debit and Credit Accounts
                    debit_account = Account.objects.get(slug="purchase")
                    credit_account = None
                    
                    if paid_by == "cash":
                        credit_account = Account.objects.get(slug="cash")
                    elif paid_by == "bank":
                        credit_account = Account.objects.get(slug="bank")
                    elif paid_by == "account-payable":
                        credit_account = Account.objects.get(slug="account-payable")
                    
                    if not credit_account:
                        raise ValueError("Invalid payment method selected.")
                    
                    # Update the journal entries (delete old entries before adding new ones)
                    JournalEntry.objects.filter(transaction=transaction_record).delete()
                    
                    # Insert updated journal entries
                    journal_entries = [
                        JournalEntry(transaction=transaction_record, account=debit_account, entry_type="debit", amount=total_amount, date=purchase.date),
                        JournalEntry(transaction=transaction_record, account=credit_account, entry_type="credit", amount=total_amount, date=purchase.date),
                    ]
                    JournalEntry.objects.bulk_create(journal_entries)
                    
                    # Handle updating the stock movements (delete old movements before adding new ones)
                    StockMovement.objects.filter(transaction=transaction_record).delete()
                    
                    # Process new stock movements for updated products
                    products = request.POST.getlist('products[]')
                    prices = request.POST.getlist('prices[]')
                    quantities = request.POST.getlist('quantities[]')
                    
                    for product_id, price, qty in zip(products, prices, quantities):
                        product_variant = ProductVariant.objects.get(id=product_id)
                        StockMovement.objects.create(
                            transaction=transaction_record,
                            account_name=debit_account,  # Assuming this acts as an account
                            product_variant=product_variant,
                            movement_type="IN",
                            quantity=int(qty),
                            amount=float(price),
                        )
                    
                    # Update the purchase record itself
                    form.save()

                    messages.success(request, 'Purchase updated successfully!')
                    return redirect('list_purchase')
            
            except Exception as e:
                messages.error(request, f"Error updating purchase: {str(e)}")
        else:
            messages.error(request, 'Error updating purchase. Please check the form and try again.')
    
    else:
        form = PurchaseForm(instance=purchase)

    context = {
        'form': form,
        'purchase': purchase,
        'suppliers': Supplier.objects.all(),
        'variants': ProductVariant.objects.all(),
        'recorded_variants': recorded_variants,
        'credit_entry': credit_entry,
        
    }

    return render(request, 'backend/purchase/edit_purchase.html', context)

@require_POST
def delete_purchase(request, pk):
    try:
        # Fetch the specified purchase object using the pk
        purchase = get_object_or_404(Purchase, pk=pk)

        # Start a database transaction to ensure atomicity
        with transaction.atomic():
            # Access the related transaction and delete related journal entries
            transaction_record = purchase.transaction
            JournalEntry.objects.filter(transaction=transaction_record).delete()

            # Delete associated stock movements
            StockMovement.objects.filter(transaction=transaction_record).delete()

            # Delete the purchase record itself
            purchase.delete()

        # Success message after deletion
        messages.info(request, 'Purchase deleted successfully.')

        # Return a success response for AJAX handling
        return JsonResponse({'success': True})

    except Exception as e:
        # Log the error if needed and return an error response for AJAX handling
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # If not a POST request, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)