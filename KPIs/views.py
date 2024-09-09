from django.shortcuts import render
from django.core.management.base import BaseCommand
from django.db.models import Sum
from .models import DailyKPI
from Orders.models import Order
from Customers.models import Customer
from django.utils import timezone
# Create your views here.


# def calculate_kpis():
#     today = timezone.now().date()
#     orders_today = Order.objects.filter(created_at__date=today)

#     total_revenue = orders_today.aggregate(Sum('total_price'))[
#         'total_price__sum'] or 0
#     total_orders = orders_today.count()
#     average_order_value = total_revenue / total_orders if total_orders > 0 else 0

#     new_customers = Customer.objects.filter(created_at__date=today).count()

#     return {
#         'total_revenue': total_revenue,
#         'average_order_value': average_order_value,
#         'total_orders': total_orders,
#         'new_customers': new_customers,
#     }


# class Command(BaseCommand):
#     help = 'Calculate daily KPIs'

#     def handle(self):
#         kpis = calculate_kpis()
#         DailyKPI.objects.create(
#             total_revenue=kpis['total_revenue'],
#             average_order_value=kpis['average_order_value'],
#             total_orders=kpis['total_orders'],
#             new_customers=kpis['new_customers'],
#         )
#         self.stdout.write(self.style.SUCCESS(
#             'Successfully calculated daily KPIs'))
