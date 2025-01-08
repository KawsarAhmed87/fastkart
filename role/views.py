from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group, Permission
from user.models import User
from .models import UserPermission
# Create your views here.
def role_create(request):
    pass
def role_list(request):
    users = User.objects.all()
    context = {
        'users': users
        }
    return render(request, 'backend/role/role_list.html', context)
def role_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    groups = Group.objects.all()
    # Fetch all permissions excluding specific models
    excluded_models = ['logentry', 'contenttype', 'session']
    all_permissions = Permission.objects.exclude(content_type__model__in=excluded_models)
    
    if request.method == 'POST':
        # Handle group updates
        selected_group_ids = request.POST.getlist('groups')
        user.groups.set(selected_group_ids)

        # Handle permission updates
        selected_permission_ids = request.POST.getlist('permissions')
        user.user_permissions.set(selected_permission_ids)

        # If you have a custom model for user permissions, update it accordingly
        # For example, assuming UserPermission has a ForeignKey to User
        UserPermission.objects.filter(user=user).delete()  # Clear existing records
        for permission_id in selected_permission_ids:
            UserPermission.objects.create(user=user, permission_id=permission_id)

        return redirect('role_list')  # Redirect to a success page or another view
    
    # Fetch the user's existing groups and permissions
    user_groups = user.groups.all()
    user_permissions = user.user_permissions.all()
    
    context = {
        'user': user,
        'groups': groups,
        'all_permissions': all_permissions,
        'user_groups': user_groups,
        'user_permissions': user_permissions,
    }
    return render(request, 'backend/role/role_update.html', context)
def role_delete(request):
    pass