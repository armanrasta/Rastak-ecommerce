from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin
from import_export.admin import ExportActionModelAdmin
from .models import Product, ProductPicture, ProductColor, Color, DiscountCode, Category

class ProductPictureInline(admin.TabularInline):
    model = ProductPicture
    extra = 1

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1

@admin.register(Product)
class ProductAdmin(DjangoQLSearchMixin, ExportActionModelAdmin):
    list_display = ['name', 'brand','category', 'quantity',
                    'price','manufacture_date', 'detail']
    inlines = [ProductPictureInline, ProductColorInline]

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(DiscountCode, ExportActionModelAdmin)