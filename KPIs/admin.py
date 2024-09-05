from django.contrib import admin
from .models import DailyKPI
from djangoql.admin import DjangoQLSearchMixin
# Register your models here

@admin.register(DailyKPI)
class DailyKPIAdmin(admin.ModelAdmin, DjangoQLSearchMixin):
    list_display = ('date', 'total_revenue', 'average_order_value', 'total_orders', 'new_customers')