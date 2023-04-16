from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', login, name='login'),
    path('', index, name='index'),

    path('product/list/', product_list, name='product_list'),
    path('product/<int:pk>/', product_details, name='product_details'),
    path('product/add/', product_add_edit, name='product_add'),
    path('product/edit/<int:pk>/', product_add_edit, name='product_edit'),
    path('product/delete/<int:pk>/', product_delete, name='product_delete'),

    path('message/list/', message_list, name='message_list'),
    path('message/<int:pk>/', message_details, name='message_details'),
    path('message/add/', message_add, name='message_add'),
    # path('message/edit/<int:pk>/', message_add, name='message_edit'),
    path('message/delete/<int:pk>/', message_delete, name='message_delete'),

    path('ctg/list/', category_list, name='ctg_list'),
    path('ctg/<int:pk>/', category_details, name='ctg_details'),
    path('ctg/add/', category_add_edit, name='ctg_add'),
    path('ctg/edit/<int:pk>/', category_add_edit, name='ctg_edit'),
    path('ctg/delete/<int:pk>/', category_delete, name='ctg_delete'),

    path('order/list/', order_list, name='order_list'),
    path('order/<int:pk>/', order_details, name='order_details'),
    path('order/delete/<int:pk>/', order_delete, name='order_delete'),

    path('users/list/', user_list, name='users_list'),
    path('user/<int:pk>/', user_detail, name='user_details'),
]