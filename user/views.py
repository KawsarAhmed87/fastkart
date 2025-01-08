from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from user.models import User
from user.forms import UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegistrationForm

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration completed.')
            return redirect('login_page')  # Replace 'login' with your desired URL name or path for the login page
    else:
        form = RegistrationForm()

    return render(request, 'backend/user/register.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')   # User is already logged in, redirect to profile
    else:
        return render(request, 'backend/user/login.html')

def login_process(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login_page')  # Redirect back to the login page if authentication fails
    else:
        return redirect('login_page')  # Redirect back to the login page if the request method is not POST

def logout_page(request):
    logout(request)
    messages.error(request, 'You have been logged out successfully.')
    return redirect('login_page')  # Redirect to the login page after logout

@login_required(login_url='login_page')
# Create your views here.
def profile(request):
    user = get_object_or_404(User, id=request.user.id)
    
    if request.method == 'POST':
        if request.user.id != user.id:
            return redirect('home')
        
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'user updated')
            return redirect('profile')
    else:
        form = UpdateUserForm(instance=user)
        
    context = {
        'user' : user
    }
    return render(request, 'backend/user/profile.html', context)


@login_required(login_url='login_page')
def change_password(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
            
        if password and confirm_password and password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, 'password updated')
            return redirect('login_page')
        else:
            messages.error(request, 'password not updated')
            return redirect('profile')
            