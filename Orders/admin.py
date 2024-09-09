from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline,]