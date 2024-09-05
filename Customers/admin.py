from django.contrib import admin
from .models import Customer, Address, Cart, CartItem

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 1
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price')
    inlines = [CartItemInline,]

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [AddressInline,]
    