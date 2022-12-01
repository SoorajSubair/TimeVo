from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(MainBanners)
admin.site.register(SubBanners)
admin.site.register(CaseShape)
admin.site.register(StrapType)
admin.site.register(ExtraImages)
admin.site.register(SalesReport)


