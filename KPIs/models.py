from django.db import models
from django.utils import timezone

# Create your models here.


class DailyKPI(models.Model):
    date = models.DateField(default=timezone.now)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField()
    new_customers = models.IntegerField()
    total_cart_abandons = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} KPI"

    @property
    def average_order_value(self):
        if self.total_orders == 0:
            return 0
        return self.total_revenue / self.total_orders


class PeriodicKPI(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField()
    total_repeats = models.IntegerField(default=0)  # Repeat Purchase Rate
    lost_customers = models.IntegerField(default=0)  # Churn Rate
    total_unique_customers = models.IntegerField(
        default=0)  # Purchase Frequency
    average_inventory = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)  # Inventory Turnover

    class Meta:
        verbose_name = "Periodic KPI"
        verbose_name_plural = "Periodic KPIs"

    def __str__(self):
        return f"KPIs since {self.start_date} unntil {self.end_date}"

    @property
    def customer_lifetime_value(self):
        if self.total_orders == 0:
            return 0
        average_order_value = self.average_order_value
        return (average_order_value * self.total_orders) - self.total_acquisition_cost

    @property
    def repeat_purchase_rate(self):
        if self.total_orders == 0:
            return 0
        return (self.total_repeats / self.total_orders) * 100

    @property
    def churn_rate(self):
        if self.total_unique_customers == 0:
            return 0
        return (self.lost_customers / self.total_unique_customers) * 100

    @property
    def purchase_frequency(self):
        if self.total_unique_customers == 0:
            return 0
        return self.total_orders / self.total_unique_customers

    @property
    def inventory_turnover(self):
        if self.average_inventory == 0:
            return 0
        return self.total_revenue / self.average_inventory
