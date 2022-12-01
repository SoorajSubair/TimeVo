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
        

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(default=date.today)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    payment = models.CharField(max_length=100, null=True, blank=True)
   

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

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='ordered_product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added =models.DateField(default=date.today)

    

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product)
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    appartment_no = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)





  
