from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomerSignUpForm, CustomerLoginForm
from django.contrib import messages
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            customer = form.save()
            # customer.backend = 'Customers.backends.CustomerBackend'
            login(request, customer)
            messages.success(
                request, 'Your account has been created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerSignUpForm()

    return render(request, 'Customers/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.is_customer:
                login(request, user)
                messages.success(request, 'Welcome!')

                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomerLoginForm()

    return render(request, 'customers/login.html', {'form': form})
