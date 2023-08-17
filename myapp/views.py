from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart,Seller,Contact
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'

def validate_product_title(request):
    seller = Seller.objects.get(email = request.session['email'])
    product_title = request.GET.get('Product_title')
    print(product_title)
    print(Product.objects.filter(seller = seller,product_title = product_title))
    data ={
        'is_taken':Product.objects.filter(seller = seller,product_title = product_title).exists()
    }
    return JsonResponse(data)

def validate_signup(request):  
    email = request.GET.get('email')
    data={
        'is_taken':User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def validate_changepassword(request):
    user = User.objects.get(email = request.session['email'])
    oldpassword = request.GET.get('oldpassword')
    print(user.fname)
    print(oldpassword)
    data={
        'is_taken':User.objects.filter(password = oldpassword,email = user.email).exists()
    }
    return JsonResponse(data)

def validate_cnewpassword(request):
    cnewpassword = request.GET.get('cnewpassword')
    newpassword = request.GET.get('newpassword')
    print('hlo')
    print(newpassword)
    if cnewpassword == newpassword:

        data={
            'is_taken':True
        }
    else:
        data={
            'is_taken':False
        }    
    return JsonResponse(data)  
    
# Payment Section Starting ----------------------------------
@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment', 
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html')
	return JsonResponse({'id': session .id})

def success(request):
    current_datetime = datetime.datetime.now()
    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    user=User()
    try:
        user=User.objects.get(email=request.session['email'])
    except:
        pass
    carts=Cart.objects.filter(user=user,payment_status=False)
    for i in carts:
        i.payment_status=True
        i.date_time = formatted_datetime
        i.save()
		
    carts=Cart.objects.filter(user=user,payment_status=False)
    request.session['cart_count']=len(carts)
    return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

# Create your views here.
def index(request):
    products = Product.objects.all()
    l = list(products)
    index_products = []
    for i in range(0,3):
        product = random.choice(l)
        index_products.append(product)
        l.remove(product)

    print(index_products)    
    return render(request,'index.html',{'index_products':index_products})


def contact(request):
    if request.method=='POST':
        Contact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            message = request.POST['message'],
        )
        msg = "Message Send Successfully"
        return render(request,'contact.html',{'msg':msg})
    else:    
        return render(request,'contact.html')
    
def signup(request):
    if request.method=='POST':
        try:
            try:
                User.objects.get(email = request.POST['email'])
                err_msg = 'Entered Email Is Already Registered'
                return render(request,'signup.html',{'err_msg':err_msg})
            except:
                Seller.objects.get(email = request.POST['email'])
                info_msg = 'Entered Email Is Already Registered In Seller System'
                return render(request,'signup.html',{'info_msg':info_msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    Organization_role = request.POST['organization_role'],
                    fname = request.POST['fname'],
                    lname = request.POST['lname'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile'],
                    address = request.POST['address'],
                    password = request.POST['password'],
                )
                succ_msg = 'Signup Done Successfully'
                return render(request,'signup.html',{'succ_msg':succ_msg})
            else:
                err_msg = 'Password & Confirmed Password Does Not Match'
                return render(request,'signup.html',{'err_msg':err_msg})
    else:      
        return render(request,'signup.html')
    

    
def signin(request):
    if request.method=='POST':
        try:
            try:
                user = User.objects.get(email = request.POST['email'])
                if user.password == request.POST['password']:
                    request.session['email'] = user.email
                    request.session['fname'] = user.fname
                    cart = Cart.objects.filter(user=user,payment_status = False)
                    request.session['cartcount'] = len(cart)
                    return redirect('index')
                else:
                    err_msg = 'Incorrect Password'
                    return render(request,'signin.html',{'err_msg':err_msg})
            except:
                seller = Seller.objects.get(email = request.POST['email'])
                if seller.password == request.POST['password']:
                    if seller.admin_access == True:
                        request.session['email'] = seller.email
                        request.session['company_name'] = seller.company_name
                        request.session['company_logo'] = seller.company_logo.url
                        return render(request,'seller-index.html')
                    else:
                        info_msg = " Account Isn't Verified Contact Admin"
                        return render(request,'signin.html',{'info_msg':info_msg})             
                else:
                    err_msg = 'Incorrect Password'
                    return render(request,'signin.html',{'err_msg':err_msg})

        except:        
            info_msg = 'Entered Email Is Not Registered So, Kindly Register'
            return render(request,'signup.html',{'info_msg':info_msg})
    else:
        return render(request,'signin.html')
    

def logout(request):
    try:
        try:
            del request.session['fname']
            del request.session['email']
            del request.session['cartcount']
            return render(request,'signin.html')
        except:
            del request.session['company_name']
            del request.session['company_logo']
            del request.session['email']
            return render(request,'signin.html')
    except:
        return render(request,'signin.html')
# ------------------------------------------- About page ---------------------------------#
def about(request):
    return render(request,'about.html')
# ------------------------------------------- shop page ----------------------------------#
def shop(request):
    products = Product.objects.all()
    return render(request,'shop.html',{'products':products})

def category_all(request):
    products = Product.objects.all()
    return render(request,'shop.html',{'products':products})

def category_clothing(request):
    products = Product.objects.filter(category = 'Clothing')
    return render(request,'shop.html',{'products':products})

def category_shoes(request):
    products = Product.objects.filter(category = 'Shoes')
    return render(request,'shop.html',{'products':products})

def category_accessories(request):
    products = Product.objects.filter(category = 'Accessories')
    return render(request,'shop.html',{'products':products})

# --------------------------------------------------- Shop Details ------------------------------#
def view_details(request,pk):
    wishlist_flag = False
    cart_flag = False 
    try:
        user = User.objects.get(email = request.session['email'])
        product = Product.objects.get(pk = pk)
        related_products = Product.objects.filter(category = product.category).exclude(pk = pk)
        try:
            Wishlist.objects.get(user = user,product = product)
            wishlist_flag = True
        except:
            pass
        try:
            Cart.objects.get(user = user,product = product,payment_status = False)
            cart_flag = True
        except:
            pass  
        return render(request,'shop-details.html',{'product':product,'related_products':related_products,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})
  
    except:
        product = Product.objects.get(pk = pk)
        related_products = Product.objects.filter(category = product.category).exclude(pk = pk)    
        return render(request,'shop-details.html',{'product':product,'related_products':related_products})

# --------------------------------------------------- Blog Page --------------------------#
def blog(request):
    return render(request,'blog.html')

def edit_profile(request):
    user = User.objects.get(email = request.session['email'])
    if request.method=='POST':
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']
        user.address = request.POST['address']
        user.save()
        succ_msg = 'Profile Updated Successfully'
        return render(request,'edit-profile.html',{'user':user,'succ_msg':succ_msg}) 
    else:    
        return render(request,'edit-profile.html',{'user':user})
    
def forget_password(request):
    if request.method=='POST':
        try:
            user = User.objects.get(email = request.POST['email'])
            otp = random.randint(1000,9999)
            subject = 'Otp To Reset Password'
            message = f'Hi {user.fname}, thank you for registering with Us {otp}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )

            succ_msg = 'OTP Send Successfullt'
            return render(request,'verify-otp.html',{'succ_msg':succ_msg,'email':user.email,'otp':otp})
        except:
            err_msg = 'Entered Email is Not Registered'
            return render(request,'forget-password.html',{'err_msg':err_msg})
    else:
        return render(request,'forget-password.html')

def verify_otp(request):
    email = request.POST['email']
    gotp = request.POST['gotp']
    otp = request.POST['otp']

    print(email)
    print(gotp)
    print(otp)

    if gotp == otp:
        return render(request,'new-password.html',{'email':email})
    else:
        err_msg = 'Incorrect OTP'
        return render(request,'verify-otp.html',{'err_msg':err_msg,'email':email,'otp':gotp})
    
def new_password(request):
    email = request.POST['email']
    np = request.POST['newpassword']    
    cnp = request.POST['cnewpassword']
    user = User.objects.get(email = email)
    if np == cnp:
        user.password = np
        user.save()
        succ_msg = 'Password Changed Successfully'
        return render(request,'signin.html',{'succ_msg':succ_msg})
    else:
        err_msg = 'Password & Confirm Password Does Not Match'
        return render(request,'new-password.html',{'err_msg':err_msg,'email':email})
def change_password(request):
    if request.method=='POST':
        user = User.objects.get(email = request.session['email'])
        oldp = request.POST['oldpassword']
        np = request.POST['newpassword']    
        cnp = request.POST['cnewpassword']

        if user.password == oldp:
            if np == cnp :
                user.password = np
                user.save()
                return redirect('logout')
            else:
                err_msg = 'Password & Confirm Password Does Not Match'
                return render(request,'change-password.html',{'err_msg':err_msg})
        else:
            err_msg = 'Old Password Does Not Match'
            return render(request,'change-password.html',{'err_msg':err_msg})
    else:
        return render(request,'change-password.html')
    
def cart(request):
    return render(request,'shopping-cart.html')    



# ------------------------------- Seller side --------------------------------------#

def seller_index(request):
    total_payment = 0
    orders_recieved = [] 
    recent_orders = []
    seller = Seller.objects.get(email = request.session['email'])
    cart = Cart.objects.filter(payment_status = True)
    for i in cart:
        if i.product.seller == seller:
            orders_recieved.append(i)
            total_payment = total_payment + i.total_price
    profit = total_payment - (0.05 * total_payment)
    for i in orders_recieved[0:4]:
        recent_orders.append(i)

    # --------------------- Related Products ------------------------
    products = Product.objects.filter(seller = seller)
    related_products = []
    l =list(products)
    for j in products[0:4]:
        random_products = random.choice(l)
        related_products.append(random_products)
        l.remove(random_products) 
    return render(request,'seller-index.html',{'total_payment':total_payment,'profit':profit,'recent_orders':recent_orders,'related_products':related_products})

def seller_registration(request):
    if request.method=='POST':
        try:
            try:
                Seller.objects.get(email = request.POST['email'])
                info_msg = 'Entered Email Is Already Registered'
                return render(request,'signin.html',{'info_msg':info_msg})
            except:
                User.objects.get(email = request.POST['email']) 
                info_msg = 'Entered Email Is Already Registered In User System'
                return render(request,'signin.html',{'info_msg':info_msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                Seller.objects.create(
                    Organization_role = request.POST['organization_role'],
                    company_logo = request.FILES['company_logo'],
                    company_name = request.POST['company_name'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    country = request.POST['country'],
                    address = request.POST['address'],
                    mobile = request.POST['mobile'],
                    password = request.POST['password'],
                )
                
                succ_msg = 'Seller Registered Successfully'
                return render(request,'signin.html',{'succ_msg':succ_msg})
            else:
                err_msg = 'Password & Confirmed Password Does Not Match'
                return render(request,'seller-registration.html',{'err_msg':err_msg})    
    else:
        return render(request,'seller-registration.html')  
    
def add_product(request):
    
    current_datetime = datetime.datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    seller = Seller.objects.get(email = request.session['email'])
    if request.method=='POST':
        product_id = request.POST['product_id']
        filtered=""
        print("Product Type : ",request.POST['product_type'])
        try:
            print("try1")
            if request.POST['category'] == 'Clothing' and request.POST['product_type']=="select":
                filtered = 'Clothing'
            elif request.POST['category'] == 'Shoes' and request.POST['product_type']=="select":
                filtered = 'Shoes'
            elif request.POST['category'] == 'Accessories' and request.POST['product_type']=="select":
                filtered = 'Accessories'
            else:
                raise Exception
            return render(request,'add-product.html',{'filtered':filtered,'product_id':product_id})
        except:
            print("Except 1")
        try:
            print("try2")
            Product.objects.get(product_id = request.POST['product_id'])
            info_msg = 'Product With This Id Is Already Registered'
            return render(request,'add-product.html',{'info_msg':info_msg})
        except:    
                print("Except 2")
                Product.objects.create(
                    seller = seller,
                    product_title = request.POST['product_title'],
                    product_description = request.POST['product_description'],
                    display_image = request.FILES['display_image'],
                    display_image1 = request.FILES['display_image1'],
                    display_image2 = request.FILES['display_image2'],
                    regular_price = request.POST['regular_price'],
                    sale_price = request.POST['sale_price'],
                    product_id = request.POST['product_id'],
                    category = request.POST['category'],
                    product_type = request.POST['product_type'],
                    collection = request.POST['collection'],
                    tags = request.POST['tags'],
                    date_time = formatted_datetime,
                )
                
                succ_msg = 'Product Added Successfully'
                return render(request,'add-product.html',{'succ_msg':succ_msg}) 
            
    else:
        return render(request,'add-product.html')
    
def seller_profile(request):
    seller = Seller.objects.get(email = request.session['email'])
    if request.method=='POST':
        seller.company_name = request.POST['company_name']
        seller.first_name = request.POST['first_name']
        seller.last_name = request.POST['last_name']
        seller.email = request.POST['email']
        seller.country = request.POST['country']
        seller.address = request.POST['address']
        seller.mobile = request.POST['mobile']
        try:
            seller.company_logo = request.FILES['company_logo']
        except:
            pass    
        seller.save()
        request.session['company_name'] = seller.company_name
        request.session['company_logo'] = seller.company_logo.url
        succ_msg = 'Profile Updated Successfully'
        return render(request,'seller_profile.html',{'seller':seller,'succ_msg':succ_msg})
    else:
        return render(request,'seller_profile.html',{'seller':seller})

def seller_security(request):
    seller = Seller.objects.get(email = request.session['email'])
    if request.method=='POST':
        if seller.password == request.POST['current_password']:
            if request.POST['new_password'] == request.POST['cnew_password'] :
                seller.password = request.POST['new_password']
                seller.save()
                succ_msg = 'Password Updated Successfully'
                return render(request,'seller_security.html',{'succ_msg':succ_msg})
            else:
                info_msg = 'Password & Confirm Password Does Not Match'
                return render(request,'seller_security.html',{'info_msg':info_msg})
        else:
            err_msg = 'Invalid Current Password'
            return render(request,'seller_security.html',{'err_msg':err_msg})
    else:
        return render(request,'seller_security.html')
    
def product_overview(request):
    seller = Seller.objects.get(email = request.session['email'])
    products = Product.objects.filter(seller = seller)
    return render(request,'product-overview.html',{'products':products})

def seller_view_by_category(request):
    seller = Seller.objects.get(email = request.session['email'])
    if request.POST['category'] == 'Clothing':
        filtered = 'Clothing'
        products = Product.objects.filter(seller = seller,category = 'Clothing')
        return render(request,'product-overview.html',{'products':products,'filtered':filtered})
    elif request.POST['category'] == 'Shoes':
        products = Product.objects.filter(seller = seller,category = 'Shoes')
        filtered = 'Shoes'
        return render(request,'product-overview.html',{'products':products,'filtered':filtered})
    elif request.POST['category'] == 'Accessories':
        products = Product.objects.filter(seller = seller,category = 'Accessories')
        filtered = 'Accessories'
        return render(request,'product-overview.html',{'products':products,'filtered':filtered})
    elif request.POST['category'] == 'All':
        products = Product.objects.filter(seller = seller)
        filtered = 'All'
        return render(request,'product-overview.html',{'products':products})
    
def seller_view_single_product(request,pk):
    seller = Seller.objects.get(email = request.session['email'])
    products = Product.objects.filter(seller = seller).exclude(pk=pk)
    product = Product.objects.get(pk=pk)
    return render(request,'seller-view-single-product.html',{'product':product,'products':products })

def view_products(request):
    seller = Seller.objects.get(email = request.session['email'])
    products = Product.objects.filter(seller = seller)
    return render(request,'view-products.html',{'products':products})

def edit_product_details(request, pk):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        product.product_title = request.POST['product_title']
        product.product_description = request.POST['product_description']
        product.regular_price = request.POST['regular_price']
        product.sale_price = request.POST['sale_price']
        product.product_id = request.POST['product_id']
        product.category = request.POST['category']
        product.product_type = request.POST['product_type']
        product.collection = request.POST['collection']
        product.tags = request.POST['tags']
        product.date_time = formatted_datetime
        try:
            product.display_image = request.FILES['display_image']
        except:
            pass
        try:    
            product.display_image1 = request.FILES['display_image1']
        except:
            pass    
        try:    
            product.display_image2 = request.FILES['display_image2']
        except:
            pass
        product.save()

        succ_msg = 'Product Details Updated Successfully'
        return render(request, 'edit_product_details.html', {'product': product, 'succ_msg': succ_msg})

    else:
        return render(request, 'edit_product_details.html', {'product': product})

def delete_product(pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('product-overview')

def add_to_wishlist(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    Wishlist.objects.create(user=user,product=product)
    return redirect('wishlist')

def wishlist(request):
    try:
        user = User.objects.get(email = request.session['email'])
        wishlist = Wishlist.objects.filter(user = user)
        print(wishlist)
        return render(request,'wishlist.html',{'wishlist':wishlist})
    except:
        return redirect('signin')

def remove_from_wishlist(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    wishlist = Wishlist.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect('wishlist')

def add_to_cart(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    qty = int(request.POST['qty'])
    single_product_total_price = product.sale_price * qty
    Cart.objects.create(
        user=user,
        product=product,
        product_price = product.sale_price,
        product_qty = qty,
        total_price = single_product_total_price,
    )

    return redirect('shopping-cart')

def shopping_cart(request): 
    try:
        net_price = 0
        user = User.objects.get(email = request.session['email'])
        cart = Cart.objects.filter(user = user,payment_status = False)
        request.session['cart_count'] = len(cart)
        for i in cart:
            net_price = net_price + i.total_price
        return render(request,'shopping-cart.html',{'cart':cart,'net_price':net_price})
    except:
        return redirect('signin')
def remove_from_cart(request,pk):
    user = User.objects.get(email = request.session['email'])
    product = Product.objects.get(pk = pk)
    cart = Cart.objects.get(user=user,product=product,payment_status = False)
    cart.delete()
    return redirect('shopping-cart')

def update_cart(request):
    qty = int(request.POST['update_qty'])
    pk = int(request.POST['product_pk'])
    cart = Cart.objects.get(pk=pk)
    cart.product_qty = qty
    single_product_total_price = cart.product.sale_price * qty
    cart.total_price = single_product_total_price
    cart.save()
    return redirect('shopping-cart')       
            
def my_orders(request):
    user = User.objects.get(email = request.session['email'])
    cart = Cart.objects.filter(user = user,payment_status = True)
    return render(request,'my-order.html',{'cart':cart})

def orders_recieved(request):
    orders_recieved = []
    total_payment = 0
    seller = Seller.objects.get(email = request.session['email'])
    cart = Cart.objects.filter(payment_status = True)
    for i in cart:
        if i.product.seller == seller:
            total_payment = total_payment + i.total_price
            orders_recieved.append(i)
    order_count = len(orders_recieved)
    print(total_payment)        
    return render(request,'orders_recieved.html',{'orders_recieved':orders_recieved,'order_count':order_count})