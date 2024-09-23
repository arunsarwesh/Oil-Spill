from django.shortcuts import render, redirect
from Ships.models import PositionReport
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

# Login view for authenticated users
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

# Sign-up view for creating new users
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

# Logout view for logging out the user
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Home page view for authenticated and unauthorized users
def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'guest.html')
    else:
        # If the user is not authenticated, render the guest home page
        return render(request, 'guest.html')

# Map view for rendering AIS data on the map
def map(request):
    if request.user.is_authenticated:
        reports = PositionReport.objects.all()
        return render(request, 'ships.html', {'reports': reports})
    else:
        # If the user is not authenticated, render the guest home page
        return render(request, 'guest.html')

def AIS(request):
    if request.user.is_authenticated:
    # Fetch all position reports from the database for logged-in users
        reports = PositionReport.objects.all()
        return render(request, 'vesel.html', {'reports': reports})
    else:
        # If the user is not authenticated, render the guest home page
        return render(request, 'guest.html')
