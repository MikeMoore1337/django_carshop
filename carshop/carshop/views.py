from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm


def home(request):
    return render(request, "home.html")


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created!')
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                messages.success(request, f'Welcome, {username}!')
                print(f'User {username} authenticated successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                print(f'Authentication failed for user {username}.')
        else:
            print(f'Form is invalid: {form.errors}')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
