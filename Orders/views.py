from django.shortcuts import redirect, get_object_or_404, render
from .models import Order, OrderItem
from Customers.models import CartItem, Cart
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from django.db import transaction
from django.db.models import F

@login_required
@transaction.atomic
def checkout(request):
    customer = request.user
    cart = get_object_or_404(Cart, customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('customers:cart_detail')

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.Customer = customer
            address.save()
            
            print("Creating order")
            order = Order(customer=customer, address=address)
            order.save()
            
            for item in cart_items:
                product = item.product
                
                if product.quantity < item.quantity:
                    return render(request, 'orders/checkout.html', {
                        'error': f"Not enough stock for {product.name}. Available: {product.quantity}, Requested: {item.quantity}",
                        'address_form': address_form,
                        'cart': cart_items,
                        'total_price': sum(i.total_price for i in cart_items)
                    })
                    
                OrderItem.objects.create(
                order=order,
                item=item.product,
                quantity=item.quantity,)
                
                product.quantity = F('quantity') - item.quantity
                product.save()
            
            cart_items.delete()
            cart.delete()
            
            return redirect('orders:order_success', order_id=order.id)
        else:
            print(address_form.errors)
    else:
        address_form = AddressForm()

    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'orders/checkout.html', {
        'address_form': address_form,
        'cart': cart_items,
        'total_price': total_price
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order
    }
    return render(request, 'orders/order_success.html', context)