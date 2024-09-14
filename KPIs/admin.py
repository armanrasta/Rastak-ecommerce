from django.contrib import admin
from .models import DailyKPI
from djangoql.admin import DjangoQLSearchMixin
from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from django.db.models import Sum, Count, F, Value, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from .models import PeriodicKPI
from Customers.models import Customer, Cart
from Orders.models import Order, OrderItem
from .forms import KPIReportForm
from django.utils.html import format_html
from import_export.admin import ExportActionMixin
from .resources import PeriodicKPIResource

# Register your models here

@admin.register(DailyKPI)
class DailyKPIAdmin(admin.ModelAdmin, DjangoQLSearchMixin):
    list_display = ('date', 'total_revenue', 'total_orders',
                    'new_customers', 'total_cart_abandons', 'average_order_value'
                    )

    change_list_template = 'admin/KPIs/DailyKPIs/change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['queryset'] = self.get_queryset(request)
        return super().changelist_view(request, extra_context=extra_context)


class PeriodicKPIAdmin(admin.ModelAdmin):
    
    resource_class = PeriodicKPIResource
    list_display = ('start_date', 'end_date', 'total_revenue', 'total_orders',
                    'total_repeats', 'lost_customers', 'total_unique_customers',
                    'average_inventory','churn_rate', 'purchase_frequency',
                    'inventory_turnover','customer_lifetime_value', 'repeat_purchase_rate')
    
    change_list_template = "admin/KPIs/PeriodicKPIs/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('report/', self.admin_site.admin_view(self.kpi_report),
                 name='periodickpi_kpi_report'),
        ]
        return custom_urls + urls

    def kpi_report(self, request):
        form = KPIReportForm()
        kpi_data = None

        if request.method == "POST":
            form = KPIReportForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']

                total_revenue = Order.objects.filter(
                    created_at__range=[start_date, end_date],
                    status=Order.StatusChoices.Done
                ).aggregate(
                    total=Coalesce(
                        Sum(
                            F('total_price') - F('items__item__bought_for') *
                            F('items__quantity'),
                            output_field=DecimalField()
                        ),
                        Value(0, output_field=DecimalField())
                    )
                )['total'] or 0

                total_orders = Order.objects.filter(
                    created_at__range=[start_date, end_date],
                    status=Order.StatusChoices.Done
                ).count()

                total_repeats = Customer.objects.annotate(
                    order_count=Count('order')
                ).filter(
                    order_count__gt=1,
                    order__created_at__range=[start_date, end_date]
                ).distinct().count()

                total_unique_customers = Customer.objects.filter(
                    order__created_at__range=[start_date, end_date]
                ).distinct().count()

                lost_customers = Customer.objects.exclude(
                    order__created_at__gte=start_date
                ).count()

                average_inventory = OrderItem.objects.filter(
                    order__created_at__range=[start_date, end_date]
                ).aggregate(
                    total_inventory=Coalesce(
                        Sum('item__quantity', output_field=IntegerField()),
                        Value(0)
                    )
                )['total_inventory'] or 0

                kpi_data = {
                    'total_revenue': total_revenue,
                    'total_orders': total_orders,
                    'total_repeats': total_repeats,
                    'lost_customers': lost_customers,
                    'total_unique_customers': total_unique_customers,
                    'average_inventory': average_inventory,
                }

                PeriodicKPI.objects.create(
                    start_date=start_date,
                    end_date=end_date,
                    total_revenue=total_revenue,
                    total_orders=total_orders,
                    total_repeats=total_repeats,
                    lost_customers=lost_customers,
                    total_unique_customers=total_unique_customers,
                    average_inventory=average_inventory,
                )

        return render(request, 'admin/KPIs/PeriodicKPIs/kpi_report.html', {
            'form': form,
            'kpi_data': kpi_data,
        })


admin.site.register(PeriodicKPI, PeriodicKPIAdmin)
