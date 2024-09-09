# products/tasks.py
from celery import shared_task
from .models import DailyKPI
from django.utils import timezone
from django.db.models import Sum, Count
from Customers.models import Customer,Cart
from Orders.models import Order

@shared_task
def calculate_daily_kpis():
    today = timezone.now().date()

    orders_today = Order.objects.filter(created_at__date=today)
    
    completed_orders = Order.objects.filter(
        status=Order.StatusChoices.Done,
        created_at__date=today
    )
    total_revenue = sum(order.total_revenue for order in completed_orders)
    
    total_orders = orders_today.count()
    new_customers_today = Customer.objects.filter(created_at__date=today).count()
    total_cart_abandons = Cart.objects.filter(created_at__date=today).count()

    DailyKPI.objects.create(
        date=today,
        total_revenue=total_revenue,
        total_orders=total_orders,
        new_customers=new_customers_today,
        total_cart_abandons=total_cart_abandons
    )