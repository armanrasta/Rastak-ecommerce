from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomerSignUpForm, CustomerLoginForm
from django.contrib import messages
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from Products.models import Product
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerSignUpForm()

    return render(request, 'Customers/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = CustomerLoginForm()

    return render(request, 'customers/login.html', {'form': form})


def customer_logout(request):
    logout(request)
    return redirect('home')


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart = get_object_or_404(Cart, customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'Customers/cart.html', context)

def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, customer=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    return redirect('customers:cart_detail')

        
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user 
    cart, created = Cart.objects.get_or_create(customer=customer)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    return redirect('customers:cart_detail')


@login_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user
    cart = get_object_or_404(Cart, customer=customer)
    
    quantity = int(request.POST.get('quantity', 1))
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('customers:cart_detail')