from django.contrib import admin
from .models import Customer, Address, Cart, CartItem
from .forms import CustomerLoginForm, CustomerSignUpForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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


class CustomerAdmin(admin.ModelAdmin):
    inlines = [AddressInline,]
    
class UserAdmin(BaseUserAdmin):
    model = Customer
    add_form = CustomerSignUpForm
    form = UserChangeForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    inlines = [AddressInline,]

admin.site.register(Customer, UserAdmin)
    