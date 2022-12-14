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
admin.site.register(Coupon)
admin.site.register(CancelItem)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(Sale)
admin.site.register(CancelSale)
admin.site.register(Wallet)
admin.site.register(ReturnRequest)


