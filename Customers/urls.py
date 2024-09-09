from django.urls import path
from .views import login_view,customer_logout, signup, cart_view, cart_remove, add_to_cart, update_cart

app_name = 'customers'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', customer_logout, name='logout'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/', cart_view, name='cart_detail'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
]