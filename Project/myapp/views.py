from django.shortcuts import render,redirect
from .models import User,Product,Comment,Review,Wishlist,Cart,Transaction
import random
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
	products=Product.objects.all()
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="user":

			st=request.POST['search']
			if st!=None:
				product=Product.objects.filter(product_company=st)
				return render(request,"index.html",{'product':product})
			else:
				products=Product.objects.all()
				return render(request,"index.html",{'products':products})
		else:
			return render(request,"seller_index.html")
	except:
		products=Product.objects.all()
		return render(request,"index.html",{'products':products})

def seller_index(request):
	products=Product.objects.all()
	return render(request,"seller_index.html",{'products':products})

def category(request):
	products=Product.objects.all()
	return render(request,"category.html",{'products':products})

def single_product(request):
	return render(request,"single-product.html")



def confirmation(request):
	return render(request,"confirmation.html")

def blog(request):
	return render(request,"blog.html")

def single_blog(request):
	return render(request,"single-blog.html")

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="user":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['lname']=user.lname
					request.session['profile_pic']=user.profile_pic.url
					wishlists=Wishlist.objects.filter(user=user)
					request.session['wishlist_count']=len(wishlists)
					carts=Cart.objects.filter(user=user,payment_status=False)
					request.session['cart_count']=len(carts)
					products=Product.objects.all()
					return redirect('index')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['lname']=user.lname
					request.session['profile_pic']=user.profile_pic.url
					return redirect("seller_index")

					
			else:
				msg="Password Is Incorrect"
				return render(request,"login.html",{'msg':msg})
		except:
			msg="Email Not Resistered"
			return render(request,"login.html",{'msg':msg})
	else:
		return render(request,"login.html")

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['lname']
		del request.session['profile_pic']
		return render(request,"login.html")
	except:
		return render(request,"login.html")
		

def signup(request):
	if request.method=="POST":
		user=User()
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.password=request.POST['password']
		user.profile_pic=request.FILES['profile_pic']
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Alredy Resister"
			return render(request,"signup.html",{'msg':msg,'user':user})
		except:
			try:
				User.objects.get(mobile=request.POST['mobile'])
				msg="Mobil Number Alredy Resister"
				return render(request,"signup.html",{'msg':msg,'user':user})
			except:
				if request.POST['password']==request.POST['cpassword']:
					User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_pic=request.FILES['profile_pic'],
						usertype=request.POST['usertype']

						)
					msg="Sign Up Successfuly"
					return render(request,"login.html",{'msg':msg})
				else:
					msg="Password & Confrim New Password Does Not Match"
					return render(request,"signup.html",{'msg':msg,'user':user})
	else:
		return render(request,"signup.html")


def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confrim New Password Does Not Match"
				return render(request,"change_password.html",{'msg':msg})
		else:
			msg="Old Password Does Not Matched"
			return render(request,"change_password.html",{'msg':msg})

	else:
		return render(request,"change_password.html")

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confrim New Password Does Not Match"
				return render(request,"seller_change_password.html",{'msg':msg})
		else:
			msg="Old Password Does Not Matched"
			return render(request,"seller_change_password.html",{'msg':msg})

	else:
		return render(request,"seller_change_password.html")


def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass

		user.save()
		msg="Profile Update Successfuly"
		request.session['fname']=user.fname
		request.session['lname']=user.lname
		request.session['mobile']=user.mobile
		request.session['address']=user.address
		request.session['profile_pic']=user.profile_pic.url
		return render(request,"profile.html",{'msg':msg,'user':user})
	else:
		return render(request,"profile.html",{'user':user})

def seller_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass

		user.save()
		msg="Profile Update Successfuly"
		request.session['fname']=user.fname
		request.session['lname']=user.lname
		request.session['mobile']=user.mobile
		request.session['address']=user.address
		request.session['profile_pic']=user.profile_pic.url
		return render(request,"seller_profile.html",{'msg':msg,'user':user})
	else:
		return render(request,"seller_profile.html",{'user':user})


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP For Forgote Password'
			message = 'Dear, '+user.fname+" "+user.lname+",\n You have reqquested for a new password. \nOTP: "+str(otp) +"\n Don't Share any one Your OTP and Password \n Thank You"
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			msg="Sent OTP"
			return render(request,"verify_otp.html",{'msg':msg,'otp':otp,'email':user.email})
		except:
			msg="Email Not Resistered"
			return render(request,"forgot_password.html",{'msg':msg})
	else:
		return render(request,"forgot_password.html")

def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']
	if otp==uotp:
		return render(request,"new_password.html",{'email':email})
	else:
		msg="Your OTP Does Not Matched"
		return render(request,"verify_otp.html",{'msg':msg,'otp':otp,'email':email})

def new_password(request):
	email=request.POST['email']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']
	if np==cnp:
		user=User.objects.get(email=email)
		if user.password==np:
			msg="Sorry You Don't Use Old Password"
			return render(request,"new_password.html",{'msg':msg,'email':email})
		else:
			user.password=np
			user.save()
			msg="Your Password Change Successfuly"
			return render(request,"login.html",{'msg':msg})
	else:
		msg="New Password & Confrim New Password Does Not Matched"
		return render(request,"new_password.html",{'msg':msg,'email':email})


def tracking(request):
	return render(request,"tracking.html")

def contact(request):
	return render(request,"contact.html")

def seller_add_product(request):
	if request.method=="POST":
		seller=User.objects.get(email=request.session['email'])
		Product.objects.create(
			seller=seller,
			product_company=request.POST['product_company'],
			product_name=request.POST['product_name'],
			product_price=request.POST['product_price'],
			product_size=request.POST['product_size'],
			product_category=request.POST['product_category'],
			product_image=request.FILES['product_image']
			)
		msg="Product Add Successfuly"
		return render(request,"seller_add_product.html",{'msg':msg})

	else:
		return render(request,"seller_add_product.html")

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,"seller_view_product.html",{'products':products})

def seller_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,"seller_product_detail.html",{'product':product})

def seller_product_update(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_company=request.POST['product_company']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_size=request.POST['product_size']
		product.product_category=request.POST['product_category']

		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg="Product Update Successfuly"
		return render(request,"seller_product_update.html",{'product':product,'msg':msg})
	else:
		return render(request,"seller_product_update.html",{'product':product})

def seller_product_back(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,"seller_product_detail.html",{'product':product})

def seller_product_delete(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	# msg="Product Delete Successfuly"
	# return render(request,"seller_view_product.html",{'msg':msg})
	return redirect(seller_view_product)

def buyer_product_detail(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	try:
		user=User.objects.get(email=request.session['email'])
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass
	try:
		user=User.objects.get(email=request.session['email'])
		Cart.objects.get(user=user,product=product,payment_status=False)
		cart_flag=True
	except:
		pass
	return render(request,"buyer_product_detail.html",{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def comment(request,pk):
	if request.method=="POST":
		product=Product.objects.get(pk=pk)
		Comment.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			message=request.POST['message']
			)
		msg="Comment sand Successfuly"
		product=Product.objects.get(pk=pk)
		comments=Comment.objects.all().order_by("-id")[:3]
		reviews=Review.objects.all().order_by("-id")[:3]

		return render(request,"buyer_product_detail.html",{'msg':msg,'comments':comments,'product':product,'reviews':reviews})
	else:
		product=Product.objects.get(pk=pk)
		comments=Comment.objects.all().order_by("-id")[:3]
		return render(request,"index.html",{'comments':comments})

def review(request,pk):
	if request.method=="POST":
		product=Product.objects.get(pk=pk)
		Review.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			message=request.POST['message']
			)
		msg="Comment sand Successfuly"
		product=Product.objects.get(pk=pk)
		reviews=Review.objects.all().order_by("-id")[:3]
		comments=Comment.objects.all().order_by("-id")[:3]

		return render(request,"buyer_product_detail.html",{'comments':comments,'msg':msg,'reviews':reviews,'product':product})
	else:
		reviews=Review.objects.all().order_by("-id")[:3]
		return render(request,"index.html",{'reviews':reviews})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('wishlist')
def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,"wishlist.html",{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')


def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		user=user,
		product=product,
		product_qty=1,
		product_price=product.product_price,
		total_price=product.product_price
		)
	return redirect('cart')

def cart(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	totalprice=0
	for item in carts:
		totalprice=totalprice+item.product.product_price*item.product_qty

	request.session['cart_count']=len(carts)
	return render(request,"cart.html",{'catrs':carts,'totalprice':totalprice})

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')


def update_cart(request):
	return render(request,"cart.html")

def checkout(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	
	subtotal=0
	for item in carts:
		subtotal=subtotal+item.product.product_price*item.product_qty
		shiping=0
		discount=0
		if subtotal <= 1000:
			discount=0
			msg="No Discount"
		elif subtotal <=2000:
			discount=5
			msg="5% Discount"
		elif subtotal <=5000:
			discount=10
			msg="10% Discount"
		elif subtotal <=10000:
			discount=20
			msg="20% Discount"
		else:
			discount=25
			msg="25% Discount"
		discount=(subtotal*discount)/100
		total=int(subtotal-discount-shiping)

	request.session['cart_count']=len(carts)
	return render(request,"checkout.html",{'msg':msg,'user':user,'catrs':carts,'subtotal':subtotal,'shiping':shiping,'discount':discount,'total':total})

def billing_genrate(request):
	return render(request,"billing_genrate.html")

def change_qty(request,pk):
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')

def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    try:
        
        amount = int(request.POST['amount'])
       
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()
    carts=Cart.objects.filter(user=user,payment_status=False)
    for i in carts:
    	i.payment_status=True
    	i.save()
    carts=Cart.objects.filter(user=user,payment_status=False)
    request.session['cart_count']=len(carts)
    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)