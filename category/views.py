from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm
from .models import Category
from django.contrib import messages
from django.core.paginator import Paginator

from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os

# Create your views here.
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Set the status explicitly based on the checkbox input
            category = form.save(commit=False)
            category.status = request.POST.get('status') == 'on'
            category.save()
            
            messages.success(request, 'Category created successfully')
            return redirect('list_category')
        else:
            messages.error(request, 'Error creating category. Please try again.')
    else:
        form = CategoryForm()
    
    parent_categories = Category.objects.filter(parent__isnull=True, status=True)

    context = {
        'link': 'create_category',
        'form': form,
        'parent_categories': parent_categories,
    }
        
    return render(request, 'backend/category/create_category.html', context)

def list_category(request):
    # Fetch categories ordered by latest created
    categories = Category.objects.order_by('-id')

    # Initialize paginator to display 10 categories per page
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)

    # Pass categories and link to context
    context = {
        'categories': categories,
        'link': 'list_category'
    }

    return render(request, 'backend/category/list_category.html', context)

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category.status = request.POST.get('status') == 'on'
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('list_category')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)

    # Determine if the current category is a parent and set parent_categories accordingly
    parent_categories = (
        Category.objects.none() if Category.objects.filter(parent=category).exists()
        else Category.objects.filter(parent__isnull=True, status=True).exclude(id=category.id)
    )

    context = {
        'form': form,
        'category': category,
        'parent_categories': parent_categories,  # Include parent categories in context
    }

    return render(request, 'backend/category/edit_category.html', context)



# @login_required  # Ensures the user is logged in
@require_POST
def delete_category(request, pk):
    try:
        # Fetch and delete the specified category
        data = get_object_or_404(Category, pk=pk)
        if data.image:
            if os.path.isfile(data.image.path):
                os.remove(data.image.path)
        data.delete()
        messages.info(request, 'Category deleted successfully.')
        
        # Return a JSON response for AJAX handling
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)