from django.urls import path
from .views import (home, products_by_category, 
                    category_list, product_detail)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('home/', home, name='home'),
    path('product/<str:product_name>/', product_detail, name='product_detail'),
    path('category/', category_list, name='category_list'),
    path('category/<slug:category_name>/',
         products_by_category, name='products_by_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
