from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ProductVariantForm
from .models import Product, ProductVariant
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import os, random, string
from django.views.decorators.http import require_POST
from category.models import Category
from brand.models import Brand
from attribute.models import Attribute, AttributeValue
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test


# @login_required(login_url='login_user')
# @user_passes_test(lambda u: u.is_staff)
def generate_random_sku(length=12):
    """Generate a random SKU consisting of uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_product(request):
    categories = Category.objects.filter(status=True)  # Get active categories
    brands = Brand.objects.filter(status=True)  # Get active brands
    attributes = Attribute.objects.filter(status=True)  # Get active attributes

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            # Generate a unique SKU
            while True:
                sku = generate_random_sku()
                if not Product.objects.filter(sku=sku).exists():
                    product.sku = sku
                    break

            product.status = request.POST.get('status') == 'on'  # Convert checkbox value to boolean
            product.save()

            messages.success(request, 'Product created successfully!')
            return redirect('list_product')
        else:
            messages.error(request, 'Error creating product. Please check the form and try again.')

    else:
        form = ProductForm()

    context = {
        'form': form,
        'categories': categories,
        'brands': brands,
        'attributes': attributes,
        'link': 'create_product'
    }
    return render(request, 'backend/product/create_product.html', context)



def edit_product(request, id):
    # Fetch the product, category, brand, and existing image
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    attributes = Attribute.objects.all()
    
    old_image_path = product.image.path if product.image else None  # Store old image path before form submission

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            # Handle the status checkbox (True if 'on', otherwise False)
            product.status = request.POST.get('status') == 'on'
            
            # Check if a new image is uploaded
            if 'image' in request.FILES:
                # Delete the old image only if a new one is uploaded
                if old_image_path and os.path.isfile(old_image_path):
                    os.remove(old_image_path)  # Remove old image from storage

            form.save()  # Save the updated product

            messages.success(request, 'Product updated successfully')
            return redirect('list_product')
        else:
            messages.error(request, 'Error updating product. Please try again.')
    else:
        form = ProductForm(instance=product)

    # Pass additional context to the template
    context = {
        'product': product,
        'form': form,
        'categories': categories,
        'brands': brands,
        'attributes': attributes,
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

def view_product(request, id):
    product = get_object_or_404(Product, id=id)

    context = {
        'product': product
    }
    return render(request, 'backend/product/view_product.html', context)
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


def create_product_variant(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    attribute_values = AttributeValue.objects.all()

    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Variant created successfully!')
            return redirect('list_product_variants')
        else:
            messages.error(request, 'Error creating Product Variant. Please check the form and try again.')
    else:
        form = ProductVariantForm()

    context = {
        'form': form,
        'product': product,
        'attribute_values': attribute_values,
        'link': 'create_product_variant'
    }
    return render(request, 'backend/product_variant/create_product_variant.html', context)



def edit_product_variant(request, id):
    product_variant = get_object_or_404(ProductVariant, id=id)
    products = Product.objects.all()
    attribute_values = AttributeValue.objects.all()
    
    old_image_path = product_variant.image.path if product_variant.image else None  

    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES, instance=product_variant)
        
        if form.is_valid():
            if 'image' in request.FILES and old_image_path and os.path.isfile(old_image_path):
                os.remove(old_image_path)

            form.save()
            messages.success(request, 'Product Variant updated successfully')
            return redirect('list_product_variants')
        else:
            messages.error(request, 'Error updating Product Variant. Please try again.')
    else:
        form = ProductVariantForm(instance=product_variant)

    context = {
        'product_variant': product_variant,
        'form': form,
        'products': products,
        'attribute_values': attribute_values,
    }
    return render(request, 'backend/product_variant/edit_product_variant.html', context)


def list_product_variants(request):
    product_variants = ProductVariant.objects.order_by('-id')
    paginator = Paginator(product_variants, 10)
    page = request.GET.get('page')
    product_variants = paginator.get_page(page)
    
    context = {
        'product_variants': product_variants,
        'link': 'list_product_variants'
    }
    return render(request, 'backend/product_variant/list_product_variants.html', context)


def view_product_variant(request, id):
    product_variant = get_object_or_404(ProductVariant, id=id)

    context = {
        'product_variant': product_variant
    }
    return render(request, 'backend/product_variant/view_product_variant.html', context)


@require_POST
def delete_product_variant(request, pk):
    if request.method == 'POST':
        try:
            product_variant = get_object_or_404(ProductVariant, pk=pk)
            if product_variant.image and os.path.isfile(product_variant.image.path):
                os.remove(product_variant.image.path)
            product_variant.delete()
            messages.info(request, 'Product Variant deleted successfully.')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)