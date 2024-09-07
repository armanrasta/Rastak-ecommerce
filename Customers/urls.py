from django.urls import path
from .views import login_view,customer_logout, signup, cart_view, cart_remove, add_to_cart

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', customer_logout, name='logout'),
    path('', add_to_cart, name='add_too_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
]