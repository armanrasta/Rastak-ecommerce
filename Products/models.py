from django.db import models
from core.models import BaseModel

class Category(BaseModel):   
    name = models.CharField(max_length=255)
    is_subcat = models.BooleanField(default=False)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcat', limit_choices_to={'is_subcat': False})
    pic = models.ImageField(upload_to="cateogry_img")
    
    def __str__(self):
        return self.name
    
#product info
class Product(BaseModel):
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    category = models.ForeignKey(Category, limit_choices_to={'is_subcat': True}, verbose_name="Selected Subcategory", on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    manufacture_date = models.DateField(verbose_name="Manufacture Date")
    manufacting_country = models.CharField(max_length=50)
    detail = models.TextField(null=True)
    bought_for= models.IntegerField()

    def __str__(self):
        return f"{self.brand} - {self.name}"
      
def image_upload_path(instance, filename):
    return f"{instance.product.brand}-{instance.product.name}/product_img/{filename}"

class ProductPicture(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to=image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super(ProductPicture, self).save(*args, **kwargs)

class Color(BaseModel):
    color = models.CharField(max_length=50)
    hex = models.CharField(max_length=7)
    
    def __str__(self):
        return self.color

class ProductColor(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.product.name} - {self.color}"
  
#discount
class DiscountCode(BaseModel):   
    code = models.TextField(max_length=16, unique=True)
    discount_type = models.CharField(max_length=10, choices=[('P', 'Percent'), ('F', 'Fixed')], null=True, blank=True)
    discount = models.IntegerField()
    availablity=models.BooleanField()
    
    def __str__(self):
        return self.code