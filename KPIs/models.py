from django.db import models
from django.utils import timezone

# Create your models here.

class DailyKPI(models.Model):
    date = models.DateField(default=timezone.now)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField()
    new_customers = models.IntegerField()
    
    def __str__(self):
        return f"{self.date} KPI"
