from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request,"index.html")

def shop(request):
	return render(request,"shop.html")

def shop_detail(request):
	return render(request,"shop_detail.html")

def like(request):
	return render(request,"like.html")

def resister(request):
	return render(request,"resister.html")

def contact(request):
	return render(request,"contact.html")

def login(request):
	return render(request,"login.html")