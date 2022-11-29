from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
import random
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):
	product=Product.objects.all()
	try:
		user=User.objects.get(email=request.session['email'])
		
		if user.usertype=="user":
			return render(request,"index.html",{'product':product})
		else:
			return render(request,"seller_index.html",{'product':product})
	except:
		return render(request,"index.html",{'product':product})

def seller_index(request):
	return render(request,"seller_index.html")

def about(request):
	return render(request,"about.html")

def cart(request):
	return render(request,"cart.html")

def checkout(request):
	return render(request,"checkout.html")

def contact_us(request):
	return render(request,"contact-us.html")

def my_account(request):
	return render(request,"my-account.html")
def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				product=Product.objects.all()
				if user.usertype=="user":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return render(request,"index.html",{'product':product})
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					wishlists=Wishlist.objects.get(user=user)
					request.session['wishlist_count']=len(wishlists)
					return render(request,"seller_index.html",{'product':product})

			else:
				msg1="Password Is Incorrect "
				return render(request,"my-account.html",{'msg1':msg1})
		except:
			msg1="Email Is Incorrect"
			return render(request,"my-account.html",{'msg1':msg1})
	else:
		return render(request,"my-account.html")

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_pic']
		return render(request,"my-account.html")
	except:
		return render(request,"my-account.html")

def signup(request):
	if request.method=="POST":
		user=User()
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Alredy Resister"
			return render(request,"my-account.html",{'msg':msg,'user':user})
		except:
			try:
				User.objects.get(mobile=request.POST['mobile'])
				msg="Mobile Number Alredy Resister"
				return render(request,"my-account.html",{'msg':msg,'user':user})
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
					msg="Create Account Successfuly"
					return render(request,"my-account.html",{'msg':msg})
				else:
					msg="Password & Confrim Password Does not Matched"
					return render(request,"my-account.html",{'msg':msg,'user':user})
	else:
		return render(request,"my-account.html")

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Your Profile Update Successfuly"
		request.session['fname']=user.fname
		request.session['lname']=user.lname
		request.session['mobile']=user.mobile
		request.session['address']=user.address
		request.session['profile_pic']=user.profile_pic.url
		return render(request,"my-account.html",{'msg':msg,'user':user})
	else:
		return render(request,"my-account.html",{'user':user})

def seller_edit_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Your Profile Update Successfuly"
		request.session['fname']=user.fname
		request.session['lname']=user.lname
		request.session['mobile']=user.mobile
		request.session['address']=user.address
		request.session['profile_pic']=user.profile_pic.url
		return render(request,"seller_edit_profile.html",{'msg':msg,'user':user})
	else:
		return render(request,"seller_edit_profile.html",{'user':user})



def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				msg1="Your Password Changed Successfuly"
				return render(request,"my-account.html",{'msg1':msg1})
			else:
				msg1="New Password & Confrim New Password Does Not Matched"
				return render(request,"my-account.html",{'msg1':msg1})
		else:
			msg1="Old Password Does Not Matched"
			return render(request,"my-account.html",{'msg1':msg1})
	else:
		return render(request,"my-account.html")


def seller_chenge_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				msg1="Your Password Changed Successfuly"
				return render(request,"seller_chenge_password.html",{'msg1':msg1})
			else:
				msg1="New Password & Confrim New Password Does Not Matched"
				return render(request,"seller_chenge_password.html",{'msg1':msg1})
		else:
			msg1="Old Password Does Not Matched"
			return render(request,"seller_chenge_password.html",{'msg1':msg1})
	else:
		return render(request,"seller_chenge_password.html")



def forgote_password(request):
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
			return render(request,"otp.html",{'msg':msg,'otp':otp,'email':user.email})
		except:
			msg="Email Not Resitered"
			return render(request,"forgote_password.html",{'msg':msg})
	else:
		
		return render(request,"forgote_password.html")

def otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	if otp==uotp:
		return render(request,"new_password.html",{'email':email})

	else:
		msg="Your OTP Does Not Matched"
		return render(request,"otp.html",{'msg':msg,'otp':otp,'email':email})

def new_password(request):
	email=request.POST['email']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']
	if np==cnp:
		user=User.objects.get(email=email)
		if user.password==np:
			msg1="Sorry You Do Not Use Your Old Password"
			return render(request,"new_password.html",{'msg1':msg1,'email':email})
		else:
			user.password=np
			user.save()
			msg1="Your Password Change Successfuly"
			return render(request,"my-account.html",{'msg1':msg1})
	else:
		msg1="Your New Password & Confrim New Password Does Not Matched"
		return render(request,"new_password.html",{'msg1':msg1,'email':email})

	return render(request,"new_password.html")
def service(request):
	return render(request,"service.html")

def shop_detail(request):
	return render(request,"shop-detail.html")

def shop(request):
	return render(request,"shop.html")

def wishlist(request):
	return render(request,"wishlist.html")

def add_product(request):
	if request.method=="POST":
		seller=User.objects.get(email=request.session["email"])
		Product.objects.create(
			seller=seller,
			product_image=request.FILES['product_image'],
			product_company=request.POST['product_company'],
			product_name=request.POST['product_name'],
			product_price=request.POST['product_price'],
			product_size=request.POST['product_size'],
			product_category=request.POST['product_category'],
			product_discription=request.POST['product_discription']
			)
		msg="Your Product Add Successfuly"
		return render(request,"add_product.html",{'msg':msg})
	else:
		return render(request,"add_product.html")

def view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,"view_product.html",{'products':products})

def detail_product(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,"detail_product.html",{'product':product})



def edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_company=request.POST['product_company']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_size=request.POST['product_size']
		product.product_category=request.POST['product_category']
		product.product_color=request.POST['product_color']
		product.product_discription=request.POST['product_discription']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg="Your Product Update Successfuly"
		return render(request,"edit_product.html",{'product':product,'msg':msg})
	else:
		return render(request,"edit_product.html",{'product':product})

def delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	# msg="Your Product Delete Successfuly"
	# return render(request,"view_product.html",{'msg':msg})
	return redirect(view_product)

def all(request):
	product=Product.objects.all()
	return render(request,"detail_product",{'product':product})

def buyer_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	return render(request,"buyer_product_detail.html",{'user':user,'product':product})

def add_to_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	Wishlist.objects.create(user=user,product=product)
	return redirect('show_wishlist')

def show_wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,"wishlist.html",{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('show_wishlist')

def add_to_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	Cart.objects.create(user=user,product=product,product_qty=1,
		product_price=product.product_price,
		total_price=product.product_price
		)
	return redirect('cart')

def cart(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user)
	subtotal=0
	for i in carts:
		subtotal=subtotal+i.product.product_price*i.product_qty
		shiping=0
		discount=0
		if subtotal < 1000:
			discount=0
			msg="No Discount"
		elif subtotal <5000:
			discount=5
			msg="5% Discount"
		elif subtotal <10000:
			discount=10
			msg="10% Discount"
		elif subtotal <20000:
			discount=12
			msg="12% Discount"
		elif subtotal <25000:
			discount=15
			msg="15% Discount"
		else:
			discount=20
			msg="20% Discount"
		discount=(subtotal*discount)/100
		tax=2
		total=subtotal+tax-discount-shiping
	return render(request,"cart.html",{'tax':tax,'carts':carts,'subtotal':subtotal,'discount':discount,'total':total,'msg':msg})

def change_qty(request,pk):
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')

def checkout(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user)
	subtotal=0
	for i in carts:
		subtotal=subtotal+i.product.product_price*i.product_qty
		shiping=0
		discount=0
		if subtotal < 1000:
			discount=0
			msg="No Discount"
		elif subtotal <5000:
			discount=5
			msg="5% Discount"
		elif subtotal <10000:
			discount=10
			msg="10% Discount"
		elif subtotal <20000:
			discount=12
			msg="12% Discount"
		elif subtotal <25000:
			discount=15
			msg="15% Discount"
		else:
			discount=20
			msg="20% Discount"
		discount=(subtotal*discount)/100
		tax=2
		total=subtotal+tax-discount-shiping
	return render(request,"checkout.html",{'tax':tax,'carts':carts,'subtotal':subtotal,'discount':discount,'total':total,'msg':msg})

def shipping_method(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user)
	subtotal=0
	for i in carts:
		subtotal=subtotal+i.product.product_price*i.product_qty
		shiping=0
		discount=0
		if subtotal < 1000:
			discount=0
			msg="No Discount"
		elif subtotal <5000:
			discount=5
			msg="5% Discount"
		elif subtotal <10000:
			discount=10
			msg="10% Discount"
		elif subtotal <20000:
			discount=12
			msg="12% Discount"
		elif subtotal <25000:
			discount=15
			msg="15% Discount"
		else:
			discount=20
			msg="20% Discount"
		discount=(subtotal*discount)/100
		tax=2
		shiping1=0
		shiping2=10
		shiping3=20

		if shipping3==request.POST['shiping1']:
			total=subtotal+20+tax-discount-shiping
		elif shiping2==request.POST['shiping2']:
			total=subtotal+10+tax-discount-shiping
		else:
			total=subtotal+tax-discount-shiping

	return render(request,"checkout.html",{'tax':tax,'carts':carts,'subtotal':subtotal,'discount':discount,'total':total,'msg':msg})

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')