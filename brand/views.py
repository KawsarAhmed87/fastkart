from django.shortcuts import render, redirect, get_object_or_404
from .forms import BrandForm
from .models import Brand

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import os
from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test


# @login_required(login_url='login_user')
# @user_passes_test(lambda u: u.is_staff)
def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.status = request.POST.get('status') == 'on'  # Set status based on checkbox
            brand.save()
            messages.success(request, 'Brand created successfully')
            return redirect('list_brand')
        else:
            messages.error(request, 'Error creating brand. Please try again.')
    else:
        form = BrandForm()
    
    context = {
        'form': form,
        'link': 'create_brand'
    }
    
    return render(request, 'backend/brand/create_brand.html', context)


def edit_brand(request, id):
    brand = get_object_or_404(Brand, id=id)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand.status = request.POST.get('status') == 'on'
            form.save()
            messages.success(request, 'Brand updated successfully')
            return redirect('list_brand')
        else:
            messages.error(request, 'Error updating brand. Please try again.')
    else:
        form = BrandForm(instance=brand)
        
    context = {
        'brand': brand,
        'form': form
    }
    return render(request, 'backend/brand/edit_brand.html', context)


def list_brand(request):
    brands = Brand.objects.order_by('-id')
    paginator = Paginator(brands, 10)
    page = request.GET.get('page')
    brands = paginator.get_page(page)
    
    context = {
        'brands': brands,
        'link': 'list_brand'
    }
    return render(request, 'backend/brand/list_brand.html', context)


@require_POST
# @login_required(login_url='login_user')
def delete_brand(request, pk):
    if request.method == 'POST':
        try:
            # Fetch and delete the specified brand
            brand = get_object_or_404(Brand, pk=pk)
            # Check if the brand has a logo and delete it from storage
            if brand.logo:
                if os.path.isfile(brand.logo.path):
                    os.remove(brand.logo.path)
            brand.delete()
            messages.info(request, 'Brand deleted successfully.')

            # Return a success response for AJAX handling
            return JsonResponse({'success': True})
        
        except Exception as e:
            # Log the error if desired, and return an error response for AJAX handling
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # If not a POST request, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
