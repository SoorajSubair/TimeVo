from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from .models import *
from django.contrib.auth import get_user_model, login, logout
from django.template.loader import render_to_string
import random
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator, EmptyPage
from .mixins import Messghandler
from django.http import JsonResponse, HttpResponseRedirect
import json
import datetime
from django.db.models import Q
from .utils import cookieCart,cartData


# Create your views here.


@never_cache
def user_home(request):

    data = cartData(request)
    cartItems = data['cartItems']

    if request.user.is_authenticated:
        try:
            if len(request.COOKIES['cart']) > 2:
                user = request.user
                data = json.loads(request.COOKIES['cart'])

                for i in data:
                    product = Product.objects.get(id = i)
                    order, created = Order.objects.get_or_create(user=user, complete=False)
                    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
                    orderItem.quantity = data[i]["quantity"]
                    orderItem.save()

                try:
                    cartItems = order.get_cart_items
                except:
                    pass

                response = HttpResponseRedirect("checkout")
                response.delete_cookie('cart')
                return response
        except:
            pass

    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)

    main_banner = MainBanners.objects.all()
    sub_banner = SubBanners.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    men = Category.objects.get(name = 'MEN')
    women = Category.objects.get(name = 'WOMEN')
    context={"products": products, "categories": categories, "men":men, "women": women, "cartItems": cartItems, "main_banner": main_banner, "sub_banner": sub_banner} 
    return render(request,'user_home.html',context)

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)

    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect(user_home)
        else:
            messages.error(request, 'Username or Password is Incorrect')
            return redirect(user_login)

    context = {"cartItems": cartItems}
    return render(request, 'user_login.html', context)

@never_cache
def user_otp(request):
    if request.user.is_authenticated:
        return redirect(user_home)

    if request.method == 'POST':
        phone = request.POST['phone']
        print(phone)
        user = CustomUser.objects.filter(phone = phone)
        if len(user) > 0:
            otp = random.randint(1000, 9999)
            print(otp)
            try:
                message_handler = Messghandler(phone, otp).send_otp_on_phone()
                request.session['phone'] = phone
                return redirect(otp_confirm)
            except:
                messages.error(request, 'OTP service is currently unavailable')
                return redirect(user_login)
        else:
            messages.error(request, 'Phone Number is not Registered')
            return redirect(user_login)

    return redirect(user_login)
    
@never_cache
def otp_confirm(request):
    if request.user.is_authenticated:
        return redirect(user_home)

    data = cartData(request)
    cartItems = data['cartItems']
    phone = request.session['phone']

    if request.method == 'POST':
        otp = request.POST['otp']
        validate = Messghandler(phone, otp).validate()
        if validate == "approved":
            user = CustomUser.objects.get(phone = phone)
            if user.is_active == True:
                login(request, user)
                return redirect(user_home)
            else:
                messages.error(request, 'Account is Temporarly Suspended!')
                return redirect(user_login)
        else:
            messages.error(request, 'OTP is Incorrect')
            return redirect(otp_confirm)

    context = {"phone": phone, "cartItems": cartItems}
    return render(request, 'otp.html', context)

@never_cache
def user_register(request):
    if 'username' in request.session:
        return redirect(user_home)

    data = cartData(request)
    cartItems = data['cartItems']

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
            return redirect(user_register)
        if not reg_username.isalnum():
            messages.error(request,'Username must contain only numbers and letters')
            return redirect(user_register)    
        if not first_name.isalpha():
            messages.error(request,'First Name must contain only letters')
            return redirect(user_register)
        if not last_name.isalpha():
            messages.error(request,'Last Name must contain only letters')
            return redirect(user_register)
        if password1 != password2:
            messages.error(request,'Passwords does not match')
            return redirect(user_register)
        if CustomUser.objects.filter(username = reg_username).exists():
            messages.error(request,'Already taken username')
            return redirect(user_register)
        if CustomUser.objects.filter(email = reg_email).exists():
            messages.error(request,'Email already exists')
            return redirect(user_register)
        if CustomUser.objects.filter(phone = phone).exists():
            messages.error(request,'Number already exists')
            return redirect(user_register)

        else:
            user_details = CustomUser.objects.create_user(username = reg_username , email = reg_email , password = password1 , first_name = first_name , last_name = last_name, phone = phone)    
            user_details.save()
            return redirect(user_login)

    context = {"cartItems": cartItems}
    return render(request, 'user_register.html', context)

@never_cache
def user_logout(request):
    logout(request)
    return redirect(user_home)

@never_cache
def list(request, id):

    data = cartData(request)
    cartItems = data['cartItems']

    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)
    
    sorting = request.GET.get('sorting', '')
    filtering = request.GET.get('filtering', '')
    category = Category.objects.get(id = id)
    products = Product.objects.filter(category = category )


    if sorting:
        products = products.order_by(sorting)
        
    if filtering == 'round' or filtering == 'square':
        products = products.filter(shape = filtering)

    if filtering == 'chain' or filtering == 'leather':
        products = products.filter(strap = filtering)

    if filtering == 'all':
        pass

    paginator = Paginator(products, 9)
    page_num = request.GET.get('page', 1)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    context={"category": category, "products": page,"cartItems": cartItems}
    return render(request, 'product_list.html', context)

@never_cache
def details(request, id):

    data = cartData(request)
    cartItems = data['cartItems']

    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)

    product = Product.objects.get(id = id)
    extraImages = ExtraImages.objects.filter(product = product)
    strap = product.strap
    shape = product.shape
    r_category = product.category
    related_product = Product.objects.filter(category = r_category, shape = shape, strap = strap).filter(~Q(id = id))
    category = product.category.name
    category_id = product.category.pk
    context={"product": product, "related_product": related_product,"category": category, "category_id": category_id, "cartItems": cartItems, "extraImages": extraImages}
    return render(request, 'product_detail.html', context)

@never_cache
def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)
        
    context = {"items":items,"order":order, "cartItems": cartItems}
    return render(request, 'cart.html', context)

@never_cache
def cart_item_delete(request, id):
    item = OrderItem.objects.get(id = id)
    item.delete()
    return redirect(cart)

@never_cache
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    user = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

@never_cache
def wishlist(request):
    return render(request, 'wishlist.html')

@never_cache
def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    address = data['address']
        
    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)

    context = {"items":items,"order":order, "cartItems": cartItems, "address": address}
    if request.user.is_authenticated:
        return render(request, 'checkout.html',context)
    else:
        return redirect(user_login)

@never_cache
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, create = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        orderItems = OrderItem.objects.filter(order = order)

        if total == float(order.get_cart_total):

            for item in orderItems:
                if item.product.quantity >= item.quantity:
                    quantity = item.quantity
                    item.product.quantity = (item.product.quantity - quantity)
                    item.product.save()
                else:
                    messages.error(request,'Sorry your order item may out of stock!')
                    print(messages.error)
                    return JsonResponse('out of stock', safe=False)

            order.complete = True
            order.date_ordered = datetime.datetime.now()
            order.status = "Order Received"
            order.payment = "Cash"
        order.save()

        address, created = ShippingAddress.objects.get_or_create(user=user)
        address.order = order
        address.address = data['shipping']['address']
        address.appartment_no = data['shipping']['appartment']
        address.city = data['shipping']['city']
        address.state = data['shipping']['state']
        address.zipcode = data['shipping']['zipcode']
        address.save()
 
    else:
        return JsonResponse('not authenticated', safe=False)

    return JsonResponse('payment complete', safe=False)

@never_cache
def process_order_paypal(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, create = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        orderItems = OrderItem.objects.filter(order = order)

        if total == float(order.get_cart_total):

            for item in orderItems:
                if item.product.quantity >= item.quantity:
                    quantity = item.quantity
                    item.product.quantity = (item.product.quantity - quantity)
                    item.product.save()
                else:
                    messages.error(request,'Sorry your order item may out of stock!')
                    print(messages.error)
                    return JsonResponse('out of stock', safe=False)

            order.complete = True
            order.date_ordered = datetime.datetime.now()
            order.status = "Order Received"
            order.payment = "Paypal"
        order.save()

        address, created = ShippingAddress.objects.get_or_create(user=user)
        address.order = order
        address.address = data['shipping']['address']
        address.appartment_no = data['shipping']['appartment']
        address.city = data['shipping']['city']
        address.state = data['shipping']['state']
        address.zipcode = data['shipping']['zipcode']
        address.save()
 
    else:
        return JsonResponse('not authenticated', safe=False)

    return JsonResponse('payment complete', safe=False)

@never_cache
def order_complete(request):

    data = cartData(request)
    cartItems = data['cartItems']

    context = {"cartItems": cartItems}
    return render(request, 'order_complete.html', context)

@never_cache
def user_account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            address, created = ShippingAddress.objects.get_or_create(user=user)
            address.address = request.POST['street']
            address.appartment_no = request.POST['apartment']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.zipcode = request.POST['zipcode']
            address.save()
            messages.success(request,'Address updated successfully!!')
            return redirect(user_account)
        else:
            if 'search_items' in request.GET:
                search_item = request.GET['search_items']
                search_product = Product.objects.filter(name__icontains=search_item)
                context = {"search_product": search_product}
                return render(request,'search_product_list.html',context)

            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            address, created = ShippingAddress.objects.get_or_create(user=user)
            orders = Order.objects.filter(user = user) 
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

            context = {"items": items, "cartItems": cartItems, "address":address, "orders": orders}
            return render(request, 'user_account.html', context)
    else:
        return redirect(user_home)


@never_cache
def user_account_update(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            email = request.POST['email']
            phone = request.POST['phone']
            if CustomUser.objects.filter(username = username).filter(~Q(username = request.user.username)).exists():
                messages.error(request,'Already taken username')
                return redirect(user_account)
            if CustomUser.objects.filter(email = email).filter(~Q(username = request.user.username)).exists():
                messages.error(request,'Email already exists')  
                return redirect(user_account)         
            if CustomUser.objects.filter(phone = phone).filter(~Q(username = request.user.username)).exists():
                messages.error(request,'Number already exists')
                return redirect(user_account)
            else:
                user = request.user
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email 
                user.phone = phone
                user.save()
                messages.success(request,'Account details updated successfully!!')
                return redirect(user_account)

@never_cache
def order_details(request, id):
    user = request.user
    order = Order.objects.get(id = id)
    orders, created = Order.objects.get_or_create(user=user, complete=False)
    address = ShippingAddress.objects.get(user = user)
    items = OrderItem.objects.filter(order = order)
    products = []
    for i in items:
        q = i.quantity
        for j in range(q):
            prod = i.product
            products.append(prod)

    cartItems = orders.get_cart_items
    if len(items) <=0 :
        return redirect(order_delete, id)

    context = {"items": items, "cartItems": cartItems, "address":address, "order": order, "products": products}
    return render(request, 'order_details.html', context)

@never_cache
def order_delete(request, id):
    order = Order.objects.filter(id = id)
    orderItems = OrderItem.objects.filter(order_id = id)
    for item in orderItems:
        quantity = item.quantity
        item.product.quantity = (item.product.quantity + quantity)
        item.product.save()
    order.delete()
    return redirect(user_account)

@never_cache
def orderItem_delete(request, p_id, o_id):
    item = OrderItem.objects.get(order_id = o_id, product_id = p_id)
    item.quantity = (item.quantity - 1)
    item.product.quantity = (item.product.quantity + 1)
    item.product.save()
    if item.quantity == 0:
        item.delete()
    else:
        item.save()
    return redirect(order_details,o_id)
