from django.shortcuts import render
from Ships.models import PositionReport
# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth.html', {'form': form, 'action': 'login'})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Signup successful!')
                return redirect('home')
            else:
                messages.error(request, 'Signup failed. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'auth.html', {'form': form, 'action': 'signup'})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')



def home_view(request):
    # Call async function using async_to_sync
    # 

    # Fetch all position reports from the database
    reports = PositionReport.objects.all()

    # Render the reports in the 'vesel.html' template
    return render(request, 'vesel.html', {'reports': reports})

# Django view to render the map with the AIS data
def map(request):
    # Since 'main.start' is an async function, you must ensure it's properly executed
    # Here you need to manage it correctly

    
    # Fetch all position reports from the database
    reports = PositionReport.objects.all()
    
    # Render the map in the 'ships.html' template
    return render(request, 'ships.html', {'reports': reports})
