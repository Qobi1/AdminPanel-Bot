from django.contrib import admin
from .views import Category, Product, User, Orders, Messages
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Orders)
admin.site.register(Messages)