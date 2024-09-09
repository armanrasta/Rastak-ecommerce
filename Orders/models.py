from django.db import models
from Customers.models import Customer
from Products.models import Product, DiscountCode
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import uuid
from core.models import BaseModel


class Order(BaseModel):
    class PaymentChoices(models.TextChoices):
        Online = "OL", ("Online")
        OnDoor = "OD", ("OnDoor")

    class StatusChoices(models.TextChoices):
        Refunded = "R", ("Refunded")
        Canceled = "C", ("Cancelled")
        InProgress = "I", ("In Progress")
        Done = "D", ("Delivered")

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountCode, null=True, blank=True, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(null=True, decimal_places=3, max_digits=20)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=StatusChoices, default=StatusChoices.InProgress, max_length=30)
    items = models.ManyToManyField("OrderItem", related_name='orders')
    address = models.ForeignKey("Customers.Address", null=False, blank=True, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0) 

    def __str__(self):
        return f'{str(self.id)}'

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
    
        self.amount = sum(item.get_cost() for item in self.items.all())
        self.total_revenue = sum(item.get_revenue() for item in self.items.all())
        
        if self.discount:
            if self.discount.type == 'F':
                self.total_price = max(self.amount - self.discount.amount, 0)
            elif self.discount.type == 'P':
                self.total_price = self.amount * (1 - self.discount.amount / 100)
        else:
            self.total_price = self.amount

        super().save(*args, **kwargs)

    def clean(self):
        if not self.address:
            raise ValidationError("Address must be provided.")

class OrderItem(BaseModel):

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    add_date = models.DateTimeField(auto_now_add=True)

    def get_cost(self):
        return self.item.price * self.quantity
    
    def get_revenue(self):
        return (self.item.price - self.item.bought_for) * self.quantity

class Transaction(BaseModel):
    SUCCESSFUL = 'S'
    NOT_SUCCESSFUL = 'NS'

    STATUS_CHOICES = [
        (SUCCESSFUL, 'Successful'),
        (NOT_SUCCESSFUL, 'Not Successful'),
    ]
    payment_method_choices = (
        ('CA', 'Cash'),
        ('CR', 'Credit'),
        ('DC', 'Debit Card')
    )
    currency_choices = (
        ('R', 'Rial'),
        ('B', 'BTC'),
        ('D', 'Dollar')
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                 MinValueValidator(0.01)])
    currency = models.CharField(
        max_length=3, choices=currency_choices, default='R')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    payment_method = models.CharField(
        max_length=2, choices=payment_method_choices, default='CR')
    transaction_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    description = models.TextField()
    refund_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.order.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.transaction_id)
