from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    image = models.ImageField(null=True , blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class MainBanners(models.Model):
    name = models.CharField(max_length = 200 , null=True , blank=True)
    image = models.ImageField(null=True , blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class SubBanners(models.Model):
    name = models.CharField(max_length = 200 , null=True , blank=True)
    image = models.ImageField(null=True , blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Category(models.Model):
    name = models.CharField(max_length = 200 , null=True , blank=True)

    def __str__(self):
        return self.name

class CaseShape(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type

class StrapType(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type

class Product(models.Model):
    name = models.CharField(max_length=200 , null=True , blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True , blank=True)
    quantity = models.IntegerField(null=True , blank=True)
    description = models.TextField(max_length = 2000)
    image = models.ImageField(null=True , blank=True)
    image2 = models.ImageField(null=True , blank=True)
    image3 = models.ImageField(null=True , blank=True)
    category = models.ForeignKey(Category , on_delete = models.CASCADE)
    shape = models.CharField(max_length=200 , null=True , blank=True)
    strap = models.CharField(max_length=200 , null=True , blank=True)
    offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=7, decimal_places=2, null=True , blank=True)
	
    def __str__(self):
        return f"{self.name}({self.category})"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def imageURL3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url

class ExtraImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True , blank=True)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class SalesReport(models.Model):
    sale = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True , blank=True)
    date = models.DateField(default=date.today,unique=True)

class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    startDate = models.DateField(default=date.today)
    endDate = models.DateField(auto_now=False, auto_now_add=False)
    is_expired = models.BooleanField(default=False)
    discount = models.PositiveIntegerField()
    maximum_discount = models.DecimalField(max_digits=7, decimal_places=2, null=True , blank=True)
    minimum_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True , blank=True)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.code)      

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(default=date.today)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    payment = models.CharField(max_length=100, null=True, blank=True)
    order_coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank=True)
    offer = models.DecimalField(max_digits=7, decimal_places=2, null=True , blank=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True , blank=True)
    cancelled = models.BooleanField(default=False)
    wallet = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    @property
    def get_cart_total(self):
        orderitems  = self.orderitem_set.all()
        total  = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems  = self.orderitem_set.all()
        total  = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_canceled_total(self):
        cancelitems  = self.cancelitem_set.all()
        total  = sum([item.get_total for item in cancelitems])
        return total

    @property
    def get_canceled_items(self):
        cancelitems  = self.cancelitem_set.all()
        total  = sum([item.quantity for item in cancelitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='ordered_product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added =models.DateField(default=date.today)

    @property
    def get_total(self):
        if self.product.offer:
            total = self.product.offer_price * self.quantity
        else:
            total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product)

class CancelItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added =models.DateField(default=date.today)
    status = models.CharField(max_length=250, null=True , blank=True)

    @property
    def get_total(self):
        if self.product.offer:
            total = self.product.offer_price * self.quantity
        else:
            total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.product)

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=False)
    appartment_no = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class ProductOffer(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    offer = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.product)

class CategoryOffer(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    offer = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.category)

class Sale(models.Model):
    date = models.DateField(default=date.today)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True , blank=True)
    item = models.CharField(max_length=250, null=True , blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True , blank=True)

    @property
    def get_total(self):
        
        if self.order.order_coupon:
            offer = self.order.offer
            discount = self.order.order_coupon.discount
            max_discount = self.order.order_coupon.maximum_discount
            if offer == max_discount:
                orderitems  = self.order.orderitem_set.all()
                no_item = 0
                for item in orderitems:
                    no_item = float(no_item) + float(item.quantity)
                
                reduce_amount = float(offer)/float(no_item)
                total = (float(self.price)-float(reduce_amount))* float(self.quantity)
            else:
                reduce_amount = (discount/100)*float(self.price)
                total = (float(self.price)-float(reduce_amount))* float(self.quantity)
        else:
            total = self.price * self.quantity
        return total

class CancelSale(models.Model):
    date = models.DateField(default=date.today)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True , blank=True)
    item = models.CharField(max_length=250, null=True , blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True , blank=True)
    status = models.CharField(max_length=250, null=True , blank=True)

class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=7, decimal_places=2, null=True , blank=True)

    def __str__(self):
        return str(self.user)

    





    





  
