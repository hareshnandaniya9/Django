from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to="profile_pic/")
	usertype=models.CharField(max_length=100,default="user")

	def __str__(self):
		return self.fname +" - "+self.lname

class Product(models.Model):
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_image=models.ImageField(upload_to="image/")
	product_company=models.CharField(max_length=100)
	product_name=models.CharField(max_length=100)
	product_price=models.PositiveIntegerField()
	product_size=models.PositiveIntegerField()
	product_category=models.CharField(max_length=100,default="other")
	product_color=models.CharField(max_length=100,default="other")
	product_discription=models.TextField()

	def __str__(self):
		return self.seller.fname+" - "+ self.product_category+" - "+self.product_name

class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_name

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	product_qty=models.PositiveIntegerField()
	product_price=models.PositiveIntegerField()
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)


	def __str__(self):
		return self.user.fname+" - "+self.product.product_name