from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierForm
from .models import Supplier
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse


def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created successfully')
            return redirect('list_supplier')
        else:
            messages.error(request, 'Error creating supplier. Please try again.')
    else:
        form = SupplierForm()
    
    context = {
        'form': form,
        'link': 'create_supplier'
    }
    
    return render(request, 'backend/supplier/create_supplier.html', context)

def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully')
            return redirect('list_supplier')
        else:
            messages.error(request, 'Error updating supplier. Please try again.')
    else:
        form = SupplierForm(instance=supplier)

    context = {
        'supplier': supplier,
        'form': form
    }
    
    return render(request, 'backend/supplier/edit_supplier.html', context)

def view_supplier(request, id):
    # Get the supplier object or return a 404 if not found
    supplier = get_object_or_404(Supplier, id=id)

    context = {
        'supplier': supplier,
        'link': 'view_supplier'
    }
    
    # Render the supplier details template
    return render(request, 'backend/supplier/view_supplier.html', context)

def list_supplier(request):
    suppliers = Supplier.objects.order_by('-id')
    paginator = Paginator(suppliers, 10)
    page = request.GET.get('page')
    suppliers = paginator.get_page(page)
    
    context = {
        'suppliers': suppliers,
        'link': 'list_supplier'
    }

    return render(request, 'backend/supplier/list_supplier.html', context)

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.info(request, 'Supplier deleted successfully.')
    return JsonResponse({'success': True})
