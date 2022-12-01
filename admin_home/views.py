from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from user_home.models import *
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
import json
from django.db.models import Q
import os
import datetime

# Create your views here.

@never_cache
def administration_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin_home)

    if request.method == 'POST':
        username = request.POST['admin_username']
        password = request.POST['admin_password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect(admin_home)
            else:
                messages.error(request, 'Username or Password is Incorrect')
                return redirect(administration_login)
        else:
            messages.error(request, 'Username or Password is Incorrect')
            return redirect(administration_login)

    return render(request, 'admin_login.html')

@never_cache
def admin_home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        sales = []
        all_sales =SalesReport.objects.all().order_by('-date')[:7]
        for sale in all_sales:
            sales.append(sale)
            
        context = {"sales": sales}
        return render(request,'admin_home.html', context)

    return redirect(administration_login)

@never_cache
def date_filter(request):
    sales = []
    sales_date = []
    sales_amount =[]
    all_sales =SalesReport.objects.all().order_by('date')
    start = request.GET.get("startdate",'')
    end = request.GET.get("enddate",'')
    format = '%Y-%m-%d'

    startdate = datetime.datetime.strptime(start, format).date()
    enddate = datetime.datetime.strptime(end, format).date()
    diff = str(enddate - startdate)
    if diff == '0:00:00':
        limit = int(diff.split(':')[0])
    else:
        limit = int(diff.split()[0])

    for i in range(limit+1):
        for sale in all_sales:
            if sale.date == startdate:
                sales_date.append(sale.date)
                sales_amount.append(sale.sale)
            
        startdate += datetime.timedelta(days=1)
        
    return JsonResponse({'sale_amount': sales_amount, 'sale_date': sales_date}, safe=False)

@never_cache
def admin_logout(request):
    logout(request)
    return redirect(administration_login)

@never_cache
def user_manage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user = CustomUser.objects.filter(is_superuser = False).order_by('id')
        context = {"user": user}
        return render(request,'user_manage.html',context)

    return redirect(administration_login)


@never_cache
def create(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            reg_username = request.POST['reg_username']
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            reg_email = request.POST['reg_email']
            phone = request.POST['phone']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if len(reg_username)<3:
                messages.error(request,'Name must be atleast 3 characters')
                return redirect(create)
            if not reg_username.isalnum():
                messages.error(request,'Username must contain only numbers and letters')
                return redirect(create)    
            if not first_name.isalpha():
                messages.error(request,'First Name must contain only letters')
                return redirect(create)
            if not last_name.isalpha():
                messages.error(request,'Last Name must contain only letters')
                return redirect(create)
            if password1 != password2:
                messages.error(request,'Passwords does not match')
                return redirect(create)
            if CustomUser.objects.filter(username = reg_username).exists():
                messages.error(request,'Already taken username')
                return redirect(create)
            if CustomUser.objects.filter(email = reg_email).exists():
                messages.error(request,'Email already exists')
                return redirect(create)
            if CustomUser.objects.filter(phone = phone).exists():
                messages.error(request,'Number already exists')
                return redirect(create)
            else:
                user_details=CustomUser.objects.create_user(username=reg_username,email=reg_email,password=password1,first_name=first_name,last_name=last_name,phone=phone)    
                user_details.save()             
                messages.success(request,'Account created successfully!!')
                return redirect(user_manage)
        
        return render(request, 'user_create.html')
        
    return redirect(administration_login)

@never_cache
def block(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = CustomUser.objects.get(id = id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect(user_manage)

    return redirect(administration_login)

@never_cache
def category_manage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        categories = Category.objects.all().order_by('id')
        context = {"categories": categories}
        return render(request, 'category_manage.html', context)

    return redirect(administration_login)

@never_cache
def cat_create(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST['name']
            if len(request.FILES) != 0:
                image = request.FILES['image']
                category = Category.objects.create(name = name, image = image)
            else:
                category = Category.objects.create(name = name)
            category.save()
            messages.success(request,'category created successfully!!')
            return redirect(category_manage)

        return render(request, 'category_create.html')

    return redirect(administration_login)

@never_cache
def cat_update(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.get(id = id)
        if request.method == 'POST':
            if len(request.FILES) != 0:
                category.image.delete()
                category.image = request.FILES['image']
            category.name = request.POST['name']
            category.save()
            messages.success(request,'category updated successfully!!')
            return redirect(category_manage)
            

        context = {"category": category}
        return render(request, 'category_update.html', context)

    return redirect(administration_login)

@never_cache
def cat_delete(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.get(id = id)
        category.image.delete()
        category.delete()
        return redirect(category_manage)

    return redirect(administration_login)

def product_manage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all().order_by('id')
        context = {"products": products}
        return render(request, 'product_manage.html', context)

    return redirect(administration_login)

@never_cache
def product_create(request):
    if request.user.is_authenticated and request.user.is_superuser:
        categories = Category.objects.all()
        context = {"categories": categories}
        if request.method == 'POST':
            name = request.POST['name']
            price = request.POST['price']
            quantity = request.POST['quantity']
            description = request.POST['description']
            image = None
            image2 = None
            image3 =None
            c_id = request.POST['category']
            category = Category.objects.get(id = c_id)
            try:
                if len(request.FILES['image1'] ) != 0:
                    image = request.FILES['image1']
            except:
                pass
            try:
                if len(request.FILES['image2'] ) != 0:
                    image2 = request.FILES['image2']
            except:
                pass
            try:
                if len(request.FILES['image3'] ) != 0:
                    image3 = request.FILES['image3']
            except:
                pass    
            product = Product.objects.create(name = name, price = price, quantity = quantity, description = description, category = category,
            image=image, image2 = image2, image3=image3)
            product.save()
            try:
                if len(request.FILES['extra_images']) != 0:
                    images = request.FILES.getlist('extra_images')
                    for image in images:
                        extra_images = ExtraImages.objects.create(
                            product = product,
                            image = image
                        )
            except:
                pass
            messages.success(request,'Product created successfully!!')
            return redirect(product_manage)

        return render(request, 'product_create.html', context)

    return redirect(administration_login)

@never_cache
def product_update(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id = id)
        categories = Category.objects.all()
        extraImages = ExtraImages.objects.filter(product = product)
        if request.method == 'POST':
            try:
                if len(request.FILES['image']) != 0:
                    product.image.delete()
                    product.image = request.FILES['image']
            except:
                pass
            try:
                if len(request.FILES['image2']) != 0:
                    product.image2.delete()
                    product.image2 = request.FILES['image2']
            except:
                pass
            try:
                if len(request.FILES['image3']) != 0:
                    product.image3.delete()
                    product.image3 = request.FILES['image3']
            except:
                pass
            try:
                if len(request.FILES['extra_images']) != 0:
                    images = request.FILES.getlist('extra_images')
                    for image in images:
                        extra_images = ExtraImages.objects.create(
                            product = product,
                            image = image
                        )
            except:
                pass

            product.name = request.POST['name']
            product.price = request.POST['price']
            product.quantity = request.POST['quantity']
            product.description = request.POST['description']
            product.shape = request.POST['shape']
            product.strap = request.POST['strap']
            c_id = request.POST['category']
            category = Category.objects.get(id = c_id)
            product.category = category
            product.save()
            messages.success(request,'Product updated successfully!!')
            return redirect(product_manage)
            

        context = {"product": product, "categories": categories,"extraImages": extraImages}
        return render(request, 'product_update.html', context)

    return redirect(administration_login)

@never_cache
def product_delete(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id = id)
        product.image.delete()
        product.delete()
        return redirect(product_manage)

    return redirect(administration_login)

@never_cache
def order_manage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all().order_by('-date_ordered')
        status = ["Order Received", "Shipped", "Out for Delivery", "Delivered", "Order Cancel"]
        context = {"orders": orders, "status":status}
        return render(request, 'order_manage.html', context)

    return redirect(administration_login)

@never_cache
def status_update(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            orderId = request.GET['orderId']
            status = request.GET['status']
            
            order = Order.objects.get(id = orderId)
            if status == 'Order Cancel':
                orderItems = OrderItem.objects.filter(order_id = orderId)
                sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
                sales.sale = sales.sale - order.get_cart_total
                sales.save()
                for item in orderItems:
                    quantity = item.quantity
                    item.product.quantity = (item.product.quantity + quantity)
                    item.product.save()
                    item.delete()
              
            order.status = status
            order.save()
            return JsonResponse('status updated', safe=False)

    return redirect(administration_login)

@never_cache
def order_view(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id = id)
        items = OrderItem.objects.filter(order = order)
        products = []
        for i in items:
            q = i.quantity
            for j in range(q):
                prod = i.product
                products.append(prod)

        if len(items) <=0 :
            order.status = 'Order Cancel'
            sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
            sales.sale = sales.sale - order.get_cart_total
            sales.save()
            order.save()
            return redirect(order_manage)

        context = {"order": order, "items": items, "products": products}
        return render(request, 'order_view.html', context)

    return redirect(administration_login)

@never_cache
def admin_orderItem_delete(request, p_id, o_id):
    if request.user.is_authenticated and request.user.is_superuser:
        item = OrderItem.objects.get(order_id = o_id, product_id = p_id)
        order = Order.objects.get(id = o_id)
        sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
        sales.sale = sales.sale - item.product.price
        sales.save()
        item.quantity = (item.quantity - 1)
        item.product.quantity = (item.product.quantity + 1)
        item.product.save()
        if item.quantity == 0:
            item.delete()
        else:
            item.save()
        return redirect(order_view,o_id)

    return redirect(administration_login)



