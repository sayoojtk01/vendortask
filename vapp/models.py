from django.db import models
from vendor.models import*


class user_register_tb(models.Model):
	username=models.CharField(max_length=100)
	email=models.CharField(max_length=200)
	password=models.CharField(max_length=100)
	phone=models.CharField(max_length=100)
	


class product_tb(models.Model):
	productname=models.CharField(max_length=255)
	oldprice=models.CharField(max_length=255)
	newprice=models.CharField(max_length=255)
	desc=models.CharField(max_length=255)
	image=models.ImageField(upload_to="product/")
	catagory=models.CharField(max_length=255)
	qty=models.CharField(max_length=255)


class cart_tb(models.Model):
	pid= models.ForeignKey(vendor_product_tb, on_delete=models.CASCADE)
	uid= models.ForeignKey(user_register_tb, on_delete=models.CASCADE)
	quantity=models.CharField(max_length=255)
	total=models.CharField(max_length=255)
	status=models.CharField(max_length=255,default="pending")



