from django.urls import path
from . import views

urlpatterns = [
    path('', views.administration_login, name='administration_login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('date_filter', views.date_filter, name='date_filter'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('user_manage', views.user_manage, name='user_manage'),
    path('block/<int:id>', views.block, name='block'),
    path('create', views.create, name='create'),
    path('category_manage', views.category_manage, name='category_manage'),
    path('cat_create', views.cat_create, name='cat_create'),
    path('cat_update/<int:id>', views.cat_update, name='cat_update'),
    path('cat_delete/<int:id>', views.cat_delete, name='cat_delete'),
    path('product_manage', views.product_manage, name='product_manage'),
    path('product_create', views.product_create, name='product_create'),
    path('product_update/<int:id>', views.product_update, name='product_update'),
    path('product_delete/<int:id>', views.product_delete, name='product_delete'),
    path('order_manage', views.order_manage, name='order_manage'),
    path('status_update', views.status_update, name='status_update'),
    path('order_view/<int:id>', views.order_view, name='order_view'),
    path('admin_orderItem_delete/<int:p_id>/<int:o_id>', views.admin_orderItem_delete, name='admin_orderItem_delete'),
    path('product_offer', views.product_offer, name='product_offer'),
    path('p_offer_create', views.p_offer_create, name='p_offer_create'),
    path('p_offer_edit/<int:id>', views.p_offer_edit, name='p_offer_edit'),
    path('p_offer_delete/<int:id>', views.p_offer_delete, name='p_offer_delete'),
    path('category_offer', views.category_offer, name='category_offer'),
    path('c_offer_create', views.c_offer_create, name='c_offer_create'),
    path('c_offer_edit/<int:id>', views.c_offer_edit, name='c_offer_edit'),
    path('c_offer_delete/<int:id>', views.c_offer_delete, name='c_offer_delete'),
    path('sales_report', views.sales_report, name='sales_report'),
    path('cancel_sale_report', views.cancel_sale_report, name='cancel_sale_report'),

]