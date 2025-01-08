from django.shortcuts import render, redirect, get_object_or_404
from .forms import AttributeForm
from .models import Attribute, AttributeValue
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

def create_attribute(request):
    if request.method == 'POST':
        form = AttributeForm(request.POST)
        if form.is_valid():
            attribute = form.save(commit=False)
            attribute.status = request.POST.get('status') == 'on'  # Set status based on checkbox
            attribute.save()

            # Save each value submitted via the dynamic inputs
            values = request.POST.getlist('values[]')  # Collect all 'values[]' inputs
            for value in values:
                if value.strip():  # Avoid saving empty values
                    AttributeValue.objects.create(attribute=attribute, value=value.strip())

            messages.success(request, 'Attribute created successfully')
            return redirect('list_attribute')
        else:
            messages.error(request, 'Error creating attribute. Please try again.')
    else:
        form = AttributeForm()

    context = {
        'form': form,
        'link': 'create_attribute'
    }
    return render(request, 'backend/attribute/create_attribute.html', context)




def edit_attribute(request, id):
    attribute = get_object_or_404(Attribute, id=id)

    if request.method == 'POST':
        form = AttributeForm(request.POST, instance=attribute)
        if form.is_valid():
            # Save the updated status field
            attribute.status = request.POST.get('status') == 'on'
            attribute = form.save(commit=False)  # Save other fields
            attribute.save()

            # Update the attribute values
            AttributeValue.objects.filter(attribute=attribute).delete()  # Clear existing values
            values = form.cleaned_data['values']
            if values:  # Ensure values is not empty
                for value in values.split(','):
                    stripped_value = value.strip()
                    if stripped_value:  # Avoid empty or whitespace-only values
                        AttributeValue.objects.create(attribute=attribute, value=stripped_value)

            messages.success(request, 'Attribute updated successfully.')
            return redirect('list_attribute')
        else:
            messages.error(request, 'Error updating attribute. Please try again.')
    else:
        # Pre-fill the form with existing values as a comma-separated string
        existing_values = ', '.join(attribute.values.values_list('value', flat=True))
        form = AttributeForm(instance=attribute, initial={'values': existing_values})
        
    context = {
        'attribute': attribute,
        'form': form,
    }
    return render(request, 'backend/attribute/edit_attribute.html', context)


def list_attribute(request):
    attributes = Attribute.objects.order_by('-id')
    paginator = Paginator(attributes, 10)
    page = request.GET.get('page')
    attributes = paginator.get_page(page)
    
    context = {
        'attributes': attributes,
        'link': 'list_attribute'
    }
    return render(request, 'backend/attribute/list_attribute.html', context)


@require_POST
def delete_attribute(request, pk):
    if request.method == 'POST':
        try:
            # Fetch and delete the specified attribute
            attribute = get_object_or_404(Attribute, pk=pk)
            attribute.delete()
            messages.info(request, 'Attribute deleted successfully.')

            # Return a success response for AJAX handling
            return JsonResponse({'success': True})
        
        except Exception as e:
            # Log the error if desired, and return an error response for AJAX handling
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # If not a POST request, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
