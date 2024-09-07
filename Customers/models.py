from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import MinLengthValidator
from Products.models import Product
from django.db.models import Sum, F



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')


        return self.create_user(username, email, password, **extra_fields)
    
            
class Customer(AbstractUser):
    phone_number = PhoneNumberField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this customer belongs to. A customer will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this customer.'
    )
    objects = CustomUserManager()
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.username


class Address(models.Model):

    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField(null=False, blank=False, max_length=30)
    city = models.CharField(null=False, blank=False, max_length=30)
    full_address = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    postal_code = models.IntegerField()
    extra_description = models.TextField()

    def __str__(self):
        return f"{self.id} - {self.Customer}"


class Cart(models.Model):

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, db_index=True)
    items = models.ManyToManyField(Product, through='CartItem')

    @property
    def total_price(self):
        return self.cartitem_set.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
        
    def __str__(self):
        return f"Cart of {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.customer.username}`s Cart"