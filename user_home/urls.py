from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_home, name='user_home'),
    path('login', views.user_login, name='user_login'),
    path('user_otp', views.user_otp, name='user_otp'),
    path('otp_confirm', views.otp_confirm, name='otp_confirm'),
    path('register', views.user_register, name='user_register'),
    path('logout', views.user_logout, name='user_logout'),
    path('list/<int:id>', views.list, name='list'),
    path('list/details/<int:id>', views.details, name='details'),
    path('account', views.user_account, name='user_account'),
    path('user_account_update', views.user_account_update, name='user_account_update'),
    path('order_details/<int:id>', views.order_details, name='order_details'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('checkout', views.checkout, name='checkout'),
    path('cart', views.cart, name='cart'),
    path('cart_item_delete/<int:id>', views.cart_item_delete, name='cart_item_delete'),
    path('update_item', views.update_item, name='update_item'),
    path('list/update_item', views.update_item, name='list_update_item'),
    path('list/details/update_item', views.update_item, name='list_details_update_item'),
    path('process_order', views.process_order, name='process_order'),
    path('order_complete', views.order_complete, name='order_complete'),
    path('order_delete/<int:id>', views.order_delete, name='order_delete'),
    path('orderItem_delete/<int:p_id>/<int:o_id>', views.orderItem_delete, name='orderItem_delete'),
]