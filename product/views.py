from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import os
from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test


# @login_required(login_url='login_user')
# @user_passes_test(lambda u: u.is_staff)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.status = request.POST.get('status') == 'on'  # Set status based on checkbox
            product.save()
            messages.success(request, 'Product created successfully')
            return redirect('list_product')
        else:
            messages.error(request, 'Error creating product. Please try again.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'link': 'create_product'
    }
    
    return render(request, 'backend/product/create_product.html', context)


def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.status = request.POST.get('status') == 'on'
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('list_product')
        else:
            messages.error(request, 'Error updating product. Please try again.')
    else:
        form = ProductForm(instance=product)
        
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'backend/product/edit_product.html', context)


def list_product(request):
    products = Product.objects.order_by('-id')
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'link': 'list_product'
    }
    return render(request, 'backend/product/list_product.html', context)


@require_POST
# @login_required(login_url='login_user')
def delete_product(request, pk):
    if request.method == 'POST':
        try:
            # Fetch and delete the specified product
            product = get_object_or_404(Product, pk=pk)
            # Check if the product has an image and delete it from storage
            if product.image:
                if os.path.isfile(product.image.path):
                    os.remove(product.image.path)
            product.delete()
            messages.info(request, 'Product deleted successfully.')

            # Return a success response for AJAX handling
            return JsonResponse({'success': True})
        
        except Exception as e:
            # Log the error if desired, and return an error response for AJAX handling
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # If not a POST request, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
