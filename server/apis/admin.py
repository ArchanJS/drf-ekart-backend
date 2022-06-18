from django.contrib import admin
from .models import User,Product

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','email','fullName','verified','phone','address','isUser','isDeliveryGuy','isSeller','createdAt','updatedAt']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','productName','description','productPrice','quantity','photo','postedby']