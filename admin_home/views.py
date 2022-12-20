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
from django.db.models import Sum

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
                request.session['admin_username'] = username
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
    if 'admin_username' in request.session:

        name = request.session['admin_username']

        sales = []
        all_sales =SalesReport.objects.all().order_by('-date')[:7][::-1]
        for sale in all_sales:
            sales.append(sale)

        daily_sale, create = SalesReport.objects.get_or_create(date = datetime.date.today())
        daily_amount = daily_sale.sale
        total_revenue = SalesReport.objects.aggregate(Sum('sale'))
        
        cancel_items = CancelItem.objects.filter(status = 'Canceled').aggregate(Sum('quantity'))
        return_items = CancelItem.objects.filter(status = 'Returned').aggregate(Sum('quantity'))
        order_items = OrderItem.objects.all().aggregate(Sum('quantity'))
        men = Category.objects.get(name = 'MEN')
        women = Category.objects.get(name = 'WOMEN')
        men_products = Product.objects.filter(category_id = men.id).count()
        women_products = Product.objects.filter(category_id = women.id).count()
           
        context = {"sales": sales, "daily_amount": daily_amount, "total_revenue":total_revenue, "cancel_items":cancel_items,"return_items":return_items,"order_items":order_items, "name": name,"men_products":men_products,"women_products":women_products}
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
    if 'admin_username' in request.session:
        request.session.flush()
    return redirect(administration_login)

@never_cache
def user_manage(request):
    if 'admin_username' in request.session:
        user = CustomUser.objects.filter(is_superuser = False).order_by('id')
        context = {"user": user}
        return render(request,'user_manage.html',context)

    return redirect(administration_login)

@never_cache
def block(request, id):
    if 'admin_username' in request.session:
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
    if 'admin_username' in request.session:
        categories = Category.objects.all().order_by('id')
        context = {"categories": categories}
        return render(request, 'category_manage.html', context)

    return redirect(administration_login)

@never_cache
def cat_create(request):
    if 'admin_username' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            categories = Category.objects.all()
            for i in categories:
                if name.lower() == i.name.lower():
                    cat = True
            if cat == True:
                messages.error(request,'category already exists')
                return redirect(cat_create)
            else:
                category = Category.objects.create(name = name)
                category.save()
                messages.success(request,'category created successfully!!')
                return redirect(category_manage)

        return render(request, 'category_create.html')

    return redirect(administration_login)

@never_cache
def cat_update(request, id):
    if 'admin_username' in request.session:
        category = Category.objects.get(id = id)
        if request.method == 'POST':
            name = request.POST['name']
            categories = Category.objects.all()
            for i in categories:
                if name.lower() == i.name.lower():
                    cat = True
            if cat == True:
                messages.error(request,'category already exists')
                return redirect(cat_update,id)
            else:
                category.name = name
                category.save()
                messages.success(request,'category updated successfully!!')
                return redirect(category_manage)
            
        context = {"category": category}
        return render(request, 'category_update.html', context)

    return redirect(administration_login)

@never_cache
def cat_delete(request, id):
    if 'admin_username' in request.session:
        category = Category.objects.get(id = id)
        category.delete()
        return redirect(category_manage)

    return redirect(administration_login)

def product_manage(request):
    if 'admin_username' in request.session:
        products = Product.objects.all().order_by('id')
        context = {"products": products}
        return render(request, 'product_manage.html', context)

    return redirect(administration_login)

@never_cache
def product_create(request):
    if 'admin_username' in request.session:
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
    if 'admin_username' in request.session:
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
    if 'admin_username' in request.session:
        product = Product.objects.get(id = id)
        product.image.delete()
        product.delete()
        return redirect(product_manage)

    return redirect(administration_login)

@never_cache
def order_manage(request):
    if 'admin_username' in request.session:
        orders = Order.objects.all().order_by('-id')
        status = ["Order Received", "Shipped", "Out for Delivery", "Delivered", "Order Cancel"]
        context = {"orders": orders, "status":status}
        return render(request, 'order_manage.html', context)

    return redirect(administration_login)

@never_cache
def status_update(request):
    if 'admin_username' in request.session:
        if request.method == 'GET':
            orderId = request.GET['orderId']
            status = request.GET['status']
            
            order = Order.objects.get(id = orderId)
            if status == 'Order Cancel':
                orderItems = OrderItem.objects.filter(order_id = orderId)
                sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
                sales.sale = float(sales.sale) - (float(order.get_cart_total)+float(order.wallet_amount))
                sales.save()

                for item in orderItems:
                    quantity = item.quantity
                    item.product.quantity = (item.product.quantity + quantity)
                    item.product.save()
                    
                    cancel_item, create = CancelItem.objects.get_or_create(order = order, product = item.product, status = 'Canceled')
                    if cancel_item.quantity == 0:
                        cancel_item.quantity = quantity
                    else:
                        cancel_item.quantity = cancel_item.quantity + quantity
                    cancel_item.save()

                    all_sale = Sale.objects.get(order = order, item = item.product.name)
                    price = float(all_sale.get_total)/float(all_sale.quantity)
                    cancel_sale = CancelSale.objects.create(order = order, item = item.product.name)
                    cancel_sale.date = datetime.date.today()
                    cancel_sale.price = price
                    cancel_sale.status = 'Canceled'
                    all_sale.quantity = all_sale.quantity - quantity

                    if order.payment != 'Cash':
                        user = request.user
                        wallet = Wallet.objects.get(user = user)
                        return_amount = float(price) * item.quantity
                        wallet.amount = float(wallet.amount) + float(return_amount)
                        wallet.save()

                    if all_sale.quantity == 0:
                        all_sale.delete()
                    else:
                        all_sale.save()
                    cancel_sale.save()

                    item.delete()

                order.cancelled = True
                order.coupon = False
                order.order_coupon = None
                order.offer = 0
                order.total = 0
              
            order.status = status
            order.save()
            return JsonResponse('status updated', safe=False)

    return redirect(administration_login)

@never_cache
def order_view(request, id):
    if 'admin_username' in request.session:
        order = Order.objects.get(id = id)
        items = OrderItem.objects.filter(order = order)
        cancel_item = CancelItem.objects.filter(order = order)
        bag_total = float(order.get_cart_total)+float(order.offer)+float(order.wallet_amount)
        products = []
        cancel_products =[]
        for i in items:
            q = i.quantity
            for j in range(q):
                prod = i.product
                products.append(prod)

        for k in cancel_item:
            c_q = k.quantity
            for l in range(c_q):
                can_prod = k.product
                cancel_products.append(can_prod)

        if len(items) <=0 :
            order.status = 'Order Cancel'
            order.cancelled = True
            sales, create = SalesReport.objects.get_or_create(date = order.date_ordered) 
            sales.sale = float(sales.sale) - (float(order.get_cart_total)+float(order.wallet_amount))
            sales.save()
            order.order_coupon = None
            order.coupon = False
            order.offer = 0
            order.total = 0
            order.save()
            
        context = {"order": order, "items": items, "products": products, "cancel_products": cancel_products, "bag_total": bag_total}
        return render(request, 'order_view.html', context)

    return redirect(administration_login)

@never_cache
def admin_orderItem_delete(request, p_id, o_id):
    if 'admin_username' in request.session:
        item = OrderItem.objects.get(order_id = o_id, product_id = p_id)
        cancel_item, create = CancelItem.objects.get_or_create(order_id = o_id, product_id = p_id, status = 'Canceled')
        order = Order.objects.get(id = o_id)
        sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
        item.quantity = (item.quantity - 1)

        if cancel_item.quantity == 0:
            cancel_item.quantity = 1
        else:
            cancel_item.quantity = cancel_item.quantity + 1
        cancel_item.save()

        all_sale = Sale.objects.get(order = order, item = item.product.name)
        price = float(all_sale.get_total)/float(all_sale.quantity)
        sales.sale = float(sales.sale) - float(price)
        sales.save()
        cancel_sale= CancelSale.objects.create(order = order, item = item.product.name)
        cancel_sale.date = datetime.date.today() 
        cancel_sale.price = price
        cancel_sale.status = 'Canceled'
        all_sale.quantity = all_sale.quantity - 1
    
        item.product.quantity = (item.product.quantity + 1)
        item.product.save()
        if item.quantity == 0:
            item.delete()
        else:
            item.save()

        if order.coupon:
            coupon = order.order_coupon
            if coupon.minimum_amount >= (float(order.get_cart_total) + float(order.offer) + float(order.wallet_amount)):
                order.total = 0
                order.offer = 0
                order.coupon = False
                order.order_coupon = None
            else:
                discount = coupon.discount
                order.offer = (discount/100)*(float(order.get_cart_total) + float(order.offer) + float(order.wallet_amount))
                if order.offer > coupon.maximum_discount:
                    order.offer = float(coupon.maximum_discount)
                # order.total = float(order.get_cart_total) - order.offer
            order.save()

        if all_sale.quantity == 0:
            all_sale.delete()
        else:
            all_sale.save()
        cancel_sale.save()

        
        return redirect(order_view,o_id)

    return redirect(administration_login)

@never_cache
def product_offer(request):

    offers = ProductOffer.objects.all().order_by('id')
    context = {"offers": offers}
    return render(request, 'product_offer.html', context)

@never_cache
def p_offer_create(request):

    products = Product.objects.all().order_by('name')

    if request.method =='POST':
        productId = request.POST['product']
        offer = request.POST['offer']
        product = Product.objects.get(id = productId)
        product_offers, create = ProductOffer.objects.get_or_create(product = product)
        product_offers.offer = int(offer) 
        product_offers.save()
        offer = int(offer)
        discount = (offer/100)*float(product.price)
        offer_price = float(product.price) - discount

        if product.offer and product.offer_price > offer_price:
            product.offer_price = offer_price

        if not product.offer:
            product.offer_price = offer_price
            product.offer = True
        
        product.save()
        messages.success(request, 'Product Offer created')
        return redirect(product_offer)

    context = {"products": products}
    return render(request, 'p_offer_create.html', context)

@never_cache
def p_offer_edit(request, id):

    product_offers = ProductOffer.objects.get(id = id)

    if request.method =='POST':
        productId = request.POST['product']
        offer = request.POST['offer']
        product = Product.objects.get(id = productId)
        product_offers, create = ProductOffer.objects.get_or_create(product = product)
        product_offers.offer = int(offer) 
        product_offers.save()
        offer = int(offer)
        discount = (offer/100)*float(product.price)
        offer_price = float(product.price) - discount

        if product.offer and product.offer_price > offer_price:
            product.offer_price = offer_price

        if not product.offer:
            product.offer_price = offer_price
            product.offer = True
        
        product.save()
        messages.success(request, 'Product Offer Updated')
        return redirect(product_offer)

    context = {"product_offer": product_offers}
    return render(request, 'p_offer_edit.html', context)

@never_cache
def p_offer_delete(request, id):

    product_offers = ProductOffer.objects.get(id = id)
    product = product_offers.product
    category = product.category
    try:
        category_offers = CategoryOffer.objects.get(category = category)
        offer = int(category_offers.offer)
        discount = (offer/100)*float(product.price)
        offer_price = float(product.price) - discount
        product.offer_price = offer_price
        product.save()
    except:
        product.offer_price = None
        product.offer = False
        product.save()
    product_offers.delete()
    return redirect(product_offer)


@never_cache
def category_offer(request):

    offers = CategoryOffer.objects.all()
    context = {"offers": offers}

    return render(request, 'category_offer.html', context)

@never_cache
def c_offer_create(request):

    categories = Category.objects.all().order_by('name')

    if request.method =='POST':
        categoryId = request.POST['category']
        offer = request.POST['offer']
        category = Category.objects.get(id = categoryId)
        products = Product.objects.filter(category = category)
        category_offers, create = CategoryOffer.objects.get_or_create(category = category)
        category_offers.offer = int(offer) 
        category_offers.save()
        
        for product in products:
            offer = int(offer)
            discount = (offer/100)*float(product.price)
            offer_price = float(product.price) - discount
            if product.offer and product.offer_price > offer_price:
                product.offer_price = offer_price

            if not product.offer:
                product.offer_price = offer_price
                product.offer = True

            product.save()

        messages.success(request,'Category Offer created')
        return redirect(category_offer)

    context = {"categories": categories}
    return render(request, 'c_offer_create.html', context)

@never_cache
def c_offer_edit(request, id):

    category_offers = CategoryOffer.objects.get(id = id)

    if request.method =='POST':
        categoryId = request.POST['category']
        offer = request.POST['offer']
        category = Category.objects.get(id = categoryId)
        products = Product.objects.filter(category = category)
        category_offers, create = CategoryOffer.objects.get_or_create(category = category)
        category_offers.offer = int(offer) 
        category_offers.save()
        
        for product in products:
            offer = int(offer)
            discount = (offer/100)*float(product.price)
            offer_price = float(product.price) - discount
            if product.offer and product.offer_price > offer_price:
                product.offer_price = offer_price

            if not product.offer:
                product.offer_price = offer_price
                product.offer = True

            product.save()

        messages.success(request,'Category Offer Updated')
        return redirect(category_offer)

    context = {"category_offer": category_offers}
    return render(request, 'c_offer_edit.html', context)

@never_cache
def c_offer_delete(request, id):

    category_offers = CategoryOffer.objects.get(id = id)
    category = category_offers.category
    products = Product.objects.filter(category = category)

    for product in products:
        try:
            product_offers = ProductOffer.objects.get(product = product)
            offer = int(product_offers.offer)
            discount = (offer/100)*float(product.price)
            offer_price = float(product.price) - discount
            product.offer_price = offer_price
            product.save()
        except:
            product.offer_price = None
            product.offer = False
            product.save()
    
    category_offers.delete()
    return redirect(category_offer)

@never_cache
def coupons(request):
    coupons = Coupon.objects.all().order_by('id')
    context = {"coupons": coupons}
    return render(request, 'coupons.html',context)

@never_cache
def coupon_create(request):
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        max_discount = request.POST['max_discount']
        min_purchase = request.POST['min_purchase']
        conditions = request.POST['conditions']
        expiry = request.POST['expiry']
        print(code)
        if Coupon.objects.filter(code = code).exists():
            messages.error(request, 'Coupon Code already exists!')
            return redirect(coupon_create)
        else:
            coupon = Coupon.objects.create(code = code, discount = discount, maximum_discount = max_discount, minimum_amount = min_purchase, description = conditions, endDate = expiry )
            coupon.save()
            messages.success(request, 'Coupon created successfully')
            return redirect(coupons)

    return render(request, 'coupon_create.html')

@never_cache
def coupon_block(request, id):
    coupon = Coupon.objects.get(id = id)
    if coupon.is_active:
        coupon.is_active = False
    else:
        coupon.is_active = True
    
    coupon.save()
    return redirect(coupons)

@never_cache
def sales_report(request):

    order = Order.objects.filter(status = 'Order Received')
    sale = Sale.objects.all().order_by('date')
    context = {"sales": sale}

    if 'datefilter' in request.POST:
        sale_date_range = []
        start = request.POST.get("start-date",'')
        end = request.POST.get("end-date",'')
        format = '%Y-%m-%d'
        try:
            startdate = datetime.datetime.strptime(start, format).date()
            enddate = datetime.datetime.strptime(end, format).date()
            diff = str(enddate - startdate)
            if diff == '0:00:00':
                limit = int(diff.split(':')[0])
            else:
                limit = int(diff.split()[0])

            for i in range(limit+1):
                for j in sale:
                    if j.date == startdate:
                        sale_date_range.append(j)
                    
                startdate += datetime.timedelta(days=1)
            
            context = {"sales": sale_date_range}
            return render(request, 'sales_report.html', context)
        except:
            return render(request, 'sales_report.html', context)

    if 'monthfilter' in request.POST:
        sale_month_range = []
        start = request.POST.get("start-month",'')
        format = '%Y-%m'
        startmonth = datetime.datetime.strptime(start, format).date()
        endmonth = datetime.datetime.strptime(start, format).date()
        try:
            try:
                endmonth = endmonth.replace(day=31)
            except :
                endmonth = endmonth.replace(day=30)
        except :
            try:
                endmonth = endmonth.replace(day=29)
            except :
                endmonth = endmonth.replace(day=28)

        diff = str(endmonth - startmonth)
        limit = int(diff.split()[0])
        for i in range(limit+1):
            for j in sale:
                if j.date == startmonth:
                    sale_month_range.append(j)
                
            startmonth += datetime.timedelta(days=1)
            
        context = {"sales": sale_month_range}
        return render(request, 'sales_report.html', context)
        
    if 'yearfilter' in request.POST:
        sale_year_range = []
        start = request.POST.get("year", '')
        format = '%Y-%m-%d'
        startyear = datetime.datetime.strptime(start, format).date()
        endyear = datetime.datetime.strptime(start, format).date()
        endyear = endyear.replace(month=12, day=31)
        diff = str(endyear - startyear)
        limit = int(diff.split()[0])
        for i in range(limit+1):
            for j in sale:
                if j.date == startyear:
                    sale_year_range.append(j)
                
            startyear += datetime.timedelta(days=1)
            
        context = {"sales": sale_year_range}
        return render(request, 'sales_report.html', context)


    return render(request, 'sales_report.html', context)

@never_cache
def cancel_sale_report(request):

    sale = CancelSale.objects.all().order_by('date')
    context = {"sales": sale}

    if 'datefilter' in request.POST:
        sale_date_range = []
        start = request.POST.get("start-date",'')
        end = request.POST.get("end-date",'')
        format = '%Y-%m-%d'
        try:
            startdate = datetime.datetime.strptime(start, format).date()
            enddate = datetime.datetime.strptime(end, format).date()
            diff = str(enddate - startdate)
            if diff == '0:00:00':
                limit = int(diff.split(':')[0])
            else:
                limit = int(diff.split()[0])

            for i in range(limit+1):
                for j in sale:
                    if j.date == startdate:
                        sale_date_range.append(j)
                    
                startdate += datetime.timedelta(days=1)
            
            context = {"sales": sale_date_range}
            return render(request, 'cancel_sale_report.html', context)
        except:
            return render(request, 'cancel_sale_report.html', context)

    if 'monthfilter' in request.POST:
        sale_month_range = []
        start = request.POST.get("start-month",'')
        format = '%Y-%m'
        startmonth = datetime.datetime.strptime(start, format).date()
        endmonth = datetime.datetime.strptime(start, format).date()
        try:
            try:
                endmonth = endmonth.replace(day=31)
            except :
                endmonth = endmonth.replace(day=30)
        except :
            try:
                endmonth = endmonth.replace(day=29)
            except :
                endmonth = endmonth.replace(day=28)

        diff = str(endmonth - startmonth)
        limit = int(diff.split()[0])
        for i in range(limit+1):
            for j in sale:
                if j.date == startmonth:
                    sale_month_range.append(j)
                
            startmonth += datetime.timedelta(days=1)
            
        context = {"sales": sale_month_range}
        return render(request, 'cancel_sale_report.html', context)
        
    if 'yearfilter' in request.POST:
        sale_year_range = []
        start = request.POST.get("year", '')
        format = '%Y-%m-%d'
        startyear = datetime.datetime.strptime(start, format).date()
        endyear = datetime.datetime.strptime(start, format).date()
        endyear = endyear.replace(month=12, day=31)
        diff = str(endyear - startyear)
        limit = int(diff.split()[0])
        for i in range(limit+1):
            for j in sale:
                if j.date == startyear:
                    sale_year_range.append(j)
                
            startyear += datetime.timedelta(days=1)
            
        context = {"sales": sale_year_range}
        return render(request, 'cancel_sale_report.html', context)

    return render(request, 'cancel_sale_report.html', context)

@never_cache
def return_request(request):
    requests = ReturnRequest.objects.all().order_by('-id')
    context = {"requests": requests}
    return render(request, 'return_request.html', context)
    
@never_cache
def orderItem_return(request):
    o_id = request.GET['o_id']
    p_id = request.GET['p_id']
    item = OrderItem.objects.get(order_id = o_id, product_id = p_id)
    product = Product.objects.get(id = p_id)
    cancel_item, create = CancelItem.objects.get_or_create(order_id = o_id, product_id = p_id, status = 'Returned')
    order = Order.objects.get(id = o_id)
    sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
    sales.sale = sales.sale - item.product.price
    sales.save()
    item.quantity = (item.quantity - 1)

    if cancel_item.quantity == 0:
        cancel_item.quantity = 1
    else:
        cancel_item.quantity = cancel_item.quantity + 1
    cancel_item.save()

    all_sale = Sale.objects.get(order = order, item = item.product.name)
    price = float(all_sale.get_total)/float(all_sale.quantity)
    cancel_sale= CancelSale.objects.create(order = order, item = item.product.name)
    cancel_sale.date = datetime.date.today() 
    cancel_sale.price = price
    cancel_sale.status = 'Returned'
    all_sale.quantity = all_sale.quantity - 1

    item.product.quantity = (item.product.quantity + 1)
    item.product.save()
    if item.quantity == 0:
        item.delete()
    else:
        item.save()

    if order.payment != 'Cash':
        user = request.GET['user']
        wallet = Wallet.objects.get(user = user) 
        wallet.amount = float(wallet.amount) + float(price)
        wallet.save()

    items = OrderItem.objects.filter(order = order)
    if len(items) <=0 :
        order.status = 'Order Cancel'
        order.cancelled = True
        sales, create = SalesReport.objects.get_or_create(date = order.date_ordered) 
        sales.sale = float(sales.sale) - (float(order.get_cart_total)+float(order.wallet_amount))
        sales.save()
        order.order_coupon = None
        order.coupon = False
        order.offer = 0
        order.total = 0
        order.save()

    if all_sale.quantity == 0:
        all_sale.delete()
    else:
        all_sale.save()
    cancel_sale.save()

    return_id = request.GET['id']
    return_request = ReturnRequest.objects.get(id = return_id).delete()

    return JsonResponse({"message":"success"}, safe=False)

