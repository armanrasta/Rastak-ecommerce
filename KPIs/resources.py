from import_export import resources
from .models import PeriodicKPI


class PeriodicKPIResource(resources.ModelResource):
    class Meta:
        model = PeriodicKPI
        fields = ('start_date', 'end_date', 'total_revenue', 'total_orders',
                  'total_repeats', 'lost_customers', 'total_unique_customers',
                  'average_inventory', 'churn_rate', 'purchase_frequency',
                  'inventory_turnover', 'customer_lifetime_value', 'repeat_purchase_rate')
        export_order = fields