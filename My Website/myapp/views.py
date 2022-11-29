from django.shortcuts import render
from .models import Contect

# Create your views here.
def index(request):
	return render(request,"index.html")

def contect(request):
	if request.method=="POST":
		Contect.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			subject=request.POST['subject'],
			message=request.POST['message']
			)
		msg="Message Sand Successfuly"
		return render(request,"contect.html",{'msg':msg})

	else:
		return render(request,"index.html")