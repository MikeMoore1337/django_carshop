from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegistrationForm


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
