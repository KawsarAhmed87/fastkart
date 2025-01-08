from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def group_create(request):
    if request.method == 'POST':
        group_name = request.POST.get('name')
        
        # Get selected permissions from request.POST
        selected_permission_ids = request.POST.getlist('permissions')

        # Create a new group
        group = Group(name=group_name)
        group.save()

        # Assign selected permissions to the group
        group.permissions.set(selected_permission_ids)

        # Redirect to the list view or another page
        return redirect('group_list')

    # Fetch all permissions excluding specific models
    excluded_models = ['group','logentry', 'contenttype', 'session']
    all_permissions = Permission.objects.exclude(content_type__model__in=excluded_models)
            
    context = {
        'all_permissions': all_permissions
    }

    return render(request, 'backend/group/group_create.html', context)

def group_list(request):
    groups = Group.objects.all()
            
    context = {
        'groups': groups
    }

    return render(request, 'backend/group/group_list.html', context)

def group_update(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    if request.method == 'POST':
        # Retrieve the updated group name from the POST data
        group_name = request.POST.get('name')

        # Get selected permissions from request.POST
        selected_permission_ids = request.POST.getlist('permissions')

        # Update the group name
        group.name = group_name
        group.save()

        # Clear existing permissions and assign selected permissions to the group
        group.permissions.clear()
        permissions = Permission.objects.filter(id__in=selected_permission_ids)
        group.permissions.set(permissions)

        # Redirect to the group list view or another page
        return redirect('group_list')

    # Fetch all permissions excluding specific models
    excluded_models = ['group','logentry', 'contenttype', 'session']
    all_permissions = Permission.objects.exclude(content_type__model__in=excluded_models)

    context = {
        'group': group,
        'all_permissions': all_permissions,
    }

    return render(request, 'backend/group/group_update.html', context)

def group_delete(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.info(request, 'Group deleted successfully.')
    return JsonResponse({'success': True})