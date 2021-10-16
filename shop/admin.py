from django.contrib import admin

from .models import Product, Contact, Orders, OrderUpdate, Reset, Replacement, Coupon
# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Reset)
admin.site.register(Replacement)
admin.site.register(Coupon)