from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name="index"),
    path('shop/',views.shop,name="shop"),
    path('shop_detail/',views.shop_detail,name="shop_detail"),
    path('like/',views.like,name="like"),
    path('resister/',views.resister,name="resister"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.login,name="login"),
]
