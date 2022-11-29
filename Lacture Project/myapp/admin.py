from django.contrib import admin
from .models import User,Product,Comment,Review,Wishlist,Cart
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Cart)




