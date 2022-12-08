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
import razorpay

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
        context = {"search_product": search_product, "cartItems": cartItems}
        return render(request,'search_product_list.html',context)

    main_banner = MainBanners.objects.all()
    sub_banner = SubBanners.objects.all()
    products = Product.objects.all()[:12]
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
        user = CustomUser.objects.filter(phone = phone)
        if len(user) > 0:
            otp = random.randint(1000, 9999)
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
            messages.success(request,'Account Successfully Registered!')
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
    products = Product.objects.filter(category = category ).order_by('name')
    filters = ["All","round","square","chain","leather"]
    sorts = ["Name: A to Z","Name: Z to A","Price: low to high","Price: high to low"]
    filtered = ''
    sorted = ''

    if sorting == 'Name: A to Z':
        products = products.order_by('name')
        sorted = sorting

    if sorting == 'Name: Z to A':
        products = products.order_by('-name')
        sorted = sorting

    if sorting == 'Price: low to high':
        products = products.order_by('price')
        sorted = sorting

    if sorting == 'Price: high to low':
        products = products.order_by('-price')
        sorted = sorting

    if filtering == 'round' or filtering == 'square':
        products = products.filter(shape = filtering)
        filtered = filtering

    if filtering == 'chain' or filtering == 'leather':
        products = products.filter(strap = filtering)
        filtered = filtering

    if filtering == 'All':
        filtered = filtering

    paginator = Paginator(products, 9)
    page_num = request.GET.get('page', 1)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    context={"category": category, "products": page,"cartItems": cartItems, "filters": filters, "sorts": sorts, "filtered": filtered, "sorted": sorted}
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
    coupons = Coupon.objects.all()

    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)

    if request.user.is_authenticated:
        if order.order_coupon:
            coupon = order.order_coupon
            if coupon.endDate < datetime.date.today():
                order.order_coupon = None
                order.offer = None
                order.total = None
                order.save()
                return redirect(cart)
            if not coupon.is_active:
                order.order_coupon = None
                order.offer = None
                order.total = None
                order.save()
                return redirect(cart)
            if coupon.minimum_amount >= order.get_cart_total:
                order.order_coupon = None
                order.offer = None
                order.total = None
                order.save()
                return redirect(cart)
            else:
                discount = coupon.discount
                order.offer = (discount/100)*float(order.get_cart_total)
                if order.offer > coupon.maximum_discount:
                    order.offer = float(coupon.maximum_discount)
                order.total = float(order.get_cart_total) - order.offer
                order.save()
                context = {"items":items,"order":order, "cartItems": cartItems, "coupons": coupons}
                return render(request, 'cart.html', context)
        
    context = {"items":items,"order":order, "cartItems": cartItems, "coupons": coupons}
    return render(request, 'cart.html', context)


@never_cache
def cart_item_delete(request, id):
    item = OrderItem.objects.get(id = id)
    item.delete()
    return redirect(cart)

@never_cache
def coupon_delete(request):
    if request.method == 'GET':
        id = request.GET['orderId']
        order = Order.objects.get(id = id)
        order.order_coupon = None
        order.offer = None
        order.total = None
        order.save()

        return JsonResponse('coupon deleted', safe=False)
    
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
    coupons = Coupon.objects.all()
    wallet,create = Wallet.objects.get_or_create(user = request.user)
    wallet_amount = wallet.amount

    if request.user.is_authenticated:
        client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_ACCOUNT_ID))
        payment = client.order.create({'amount': float(order.get_cart_total) * 100, 'currency': 'INR' , 'payment_capture': 1})
        order.transaction_id = payment['id']
        order.save()
        context = {"items":items,"order":order, "cartItems": cartItems, "address": address, "payment": payment, "coupons": coupons, "wallet": wallet_amount}
    
    if request.method == 'POST':
        if 'address_create' in request.POST:
            address = ShippingAddress.objects.create(user = request.user)
            address.name = request.POST['name']
            address.phone = request.POST['phone']
            address.address = request.POST['street']
            address.appartment_no = request.POST['appartment']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.zipcode = request.POST['zipcode']
            address.save()
            messages.success(request,'Address created successfully!!')
            return redirect(checkout)

        if 'coupon_apply' in request.POST:
            code = request.POST['coupon']
            try:
                coupon = Coupon.objects.get(code = code)
                order.order_coupon = coupon
            except:
                messages.error(request, "Coupon doesn't Exist")
                return redirect(checkout)
            if coupon.endDate < datetime.date.today():
                messages.error(request, "Coupon is Expired")
                return redirect(checkout)
            if not coupon.is_active:
                messages.error(request, "Sorry This Coupon is Not Available")
                return redirect(checkout)
            if coupon.minimum_amount >= order.get_cart_total:
                messages.error(request, "Need to Buy Minimum "+str(coupon.minimum_amount)+" to Avail this Offer")
                return redirect(checkout)
            else:
                discount = coupon.discount
                order.offer = (discount/100)*float(order.get_cart_total)
                if order.offer > coupon.maximum_discount:
                    order.offer = float(coupon.maximum_discount)
                order.total = float(order.get_cart_total) - order.offer
                order.save()
                payment = client.order.create({'amount': float(order.total) * 100, 'currency': 'INR' , 'payment_capture': 1})
                messages.success(request, "Coupon Applied")
                context = {"items":items, "order":order, "cartItems": cartItems, "address": address, "payment": payment, "coupons": coupons, "code": code, "wallet": wallet_amount}
                return render(request, 'checkout.html', context)

    if 'search_items' in request.GET:
        search_item = request.GET['search_items']
        search_product = Product.objects.filter(name__icontains=search_item)
        context = {"search_product": search_product}
        return render(request,'search_product_list.html',context)

    if request.user.is_authenticated:
        return render(request, 'checkout.html',context)
    else:
        return redirect(user_login)

# @never_cache
# def redeem_wallet(request):

#     data = cartData(request)
#     order = data['order']
#     wallet = Wallet.objects.get(user = request.user)
#     wallet_amount = wallet.amount
#     if order.order_coupon:
#         if wallet_amount > order.total:
#             wallet_amount = float(wallet_amount) - float(order.total)
#             order.total = 0
#             order.wallet = True
#             wallet.save()
#             order.save()
#         else:
#             order.total = float(order.total) - float(wallet_amount)
#             wallet_amount = 0
#             order.wallet = True
#             wallet.save()
#             order.save()
#     else:
#         if wallet_amount > order.total:
#             order.total = order.get_cart_total
#             wallet_amount = float(wallet_amount) - float(order.total)
#             order.total = 0
#             order.wallet = True
#             wallet.save()
#             order.save()
#         else:
#             order.total = order.get_cart_total
#             order.total = float(order.total) - float(wallet_amount) 
#             wallet_amount = 0
#             order.wallet = True
#             wallet.save()
#             order.save()

#     return redirect(checkout)

@never_cache
def process_order(request):
    if not request.user.is_authenticated:
        return redirect(user_home)

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, create = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        addressId = data['shipping']
        address = ShippingAddress.objects.get(id = addressId)
        order.transaction_id = transaction_id
        orderItems = OrderItem.objects.filter(order = order)

        if order.order_coupon:
            order_total = float(order.total)
        else:
            order_total = float(order.get_cart_total)

        if total == order_total: 
            for item in orderItems:
                if item.product.quantity >= item.quantity:
                    quantity = item.quantity
                    item.product.quantity = (item.product.quantity - quantity)
                    item.product.save()
                else:
                    messages.error(request,'Sorry your order item may out of stock!')
                    return JsonResponse('out of stock', safe=False)

            order.complete = True
            order.date_ordered = datetime.datetime.today()
            order.status = "Order Received"
            order.payment = data['method']
            address.order = order
            address.save()
        order.save()

        if order.complete == True:
            sales, create = SalesReport.objects.get_or_create(date = datetime.date.today())
            if sales.sale == None:
                if order.order_coupon:
                    sales.sale = order.total
                else:
                    sales.sale = order.get_cart_total
            else:
                if order.order_coupon:
                    sales.sale = sales.sale + order.total
                else:
                    sales.sale = sales.sale + order.get_cart_total
            sales.save()

            for item in orderItems:
                all_sale_report = Sale.objects.create(date = datetime.date.today())
                all_sale_report.order = item.order
                all_sale_report.item = item.product.name
                all_sale_report.quantity = item.quantity
                all_sale_report.price = item.product.price
                all_sale_report.save()

    if order.complete == True:
        return JsonResponse('payment complete', safe=False)
    else:
        return JsonResponse('not completed', safe=False)

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
            id = request.POST['id']
            address = ShippingAddress.objects.get(id=id)
            address.name = request.POST['name']
            address.phone = request.POST['phone']
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
            address = ShippingAddress.objects.filter(user=user)
            wallet = Wallet.objects.get(user = user)
            orders = Order.objects.filter(user = user) 
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            sale = Sale.objects.filter(order = order)

            context = {"items": items, "cartItems": cartItems, "address":address, "orders": orders, "wallet": wallet, "sale": sale}
            return render(request, 'user_account.html', context)
    else:
        return redirect(user_home)

@never_cache
def address_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            address = ShippingAddress.objects.create(user=user)
            address.name = request.POST['name']
            address.phone = request.POST['phone']
            address.address = request.POST['street']
            address.appartment_no = request.POST['apartment']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.zipcode = request.POST['zipcode']
            address.save()
            messages.success(request,'Address created successfully!!')
            return redirect(user_account)
        else:
            return redirect(user_account)
    
    return redirect(user_home)

@never_cache
def address_delete(request,id):
    if request.user.is_authenticated:
        address = ShippingAddress.objects.get(id = id)
        address.delete()
        return redirect(user_account)

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
            try:
                if len(request.FILES['profile_image'] ) != 0:
                    request.user.image.delete()
                    image = request.FILES['profile_image']
            except:
                pass
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
                user.image = image
                user.save()
                messages.success(request,'Account details updated successfully!!')
                return redirect(user_account)

@never_cache
def order_details(request, id):
    user = request.user
    order = Order.objects.get(id = id)
    orders, created = Order.objects.get_or_create(user=user, complete=False)
    address = ShippingAddress.objects.filter(user = user)
    items = OrderItem.objects.filter(order = order)
    cancel_item = CancelItem.objects.filter(order = order)
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

    cartItems = orders.get_cart_items
    if len(items) <=0 :
        order.status = 'Order Cancel'
        order.cancelled = True
        sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
        if order.order_coupon:
            sales.sale = sales.sale - order.total
        else:
            sales.sale = sales.sale - order.get_cart_total
        sales.save()
        order.order_coupon = None
        order.offer = None
        order.total = None
        order.save()

    context = {"items": items, "cartItems": cartItems, "address":address, "order": order, "products": products, "cancel_products": cancel_products}
    return render(request, 'order_details.html', context)

@never_cache
def order_delete(request, id):
    order = Order.objects.get(id = id)
    orderItems = OrderItem.objects.filter(order_id = id)
    sales, create = SalesReport.objects.get_or_create(date = order.date_ordered)
    if order.order_coupon:
        sales.sale = sales.sale - order.total
    else:
        sales.sale = sales.sale - order.get_cart_total
    sales.save()

    for item in orderItems:
        quantity = item.quantity
        item.product.quantity = (item.product.quantity + quantity)
        item.product.save()
        item.save()

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

    order.status = 'Order Cancel'
    order.cancelled = True
    order.order_coupon = None
    order.offer = None
    order.total = None
    order.save()
    return redirect(user_account)

@never_cache
def orderItem_delete(request, p_id, o_id):
    item = OrderItem.objects.get(order_id = o_id, product_id = p_id)
    cancel_item, create = CancelItem.objects.get_or_create(order_id = o_id, product_id = p_id, status = 'Canceled')
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
    cancel_sale.status = 'Canceled'
    all_sale.quantity = all_sale.quantity - 1
    
    item.product.quantity = (item.product.quantity + 1)
    item.product.save()
    if item.quantity == 0:
        item.delete()
    else:
        item.save()

    if order.order_coupon:
        coupon = order.order_coupon
        if coupon.minimum_amount >= order.get_cart_total:
            order.total = order.get_cart_total
            order.order_coupon = None
        else:
            discount = coupon.discount
            order.offer = (discount/100)*float(order.get_cart_total)
            if order.offer > coupon.maximum_discount:
                order.offer = float(coupon.maximum_discount)
            order.total = float(order.get_cart_total) - order.offer
        order.save()

    if order.payment != 'Cash':
        user = request.user
        wallet = Wallet.objects.get(user = user)
        wallet.amount = float(wallet.amount) + float(price)
        wallet.save()

    if all_sale.quantity == 0:
        all_sale.delete()
    else:
        all_sale.save()
    cancel_sale.save()

        
    return redirect(order_details,o_id)

@never_cache
def orderItem_return(request, p_id, o_id):
    item = OrderItem.objects.get(order_id = o_id, product_id = p_id)
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
        user = request.user
        wallet = Wallet.objects.get(user = user) 
        wallet.amount = float(wallet.amount) + float(price)
        wallet.save()

    if all_sale.quantity == 0:
        all_sale.delete()
    else:
        all_sale.save()
    cancel_sale.save()

    return redirect(order_details,o_id)
