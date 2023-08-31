from django.db import models

# Create your models here.


class vendor_register_tb(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=200)
	password=models.CharField(max_length=100)
	bank=models.CharField(max_length=100)
	ifsc=models.CharField(max_length=100)
	place=models.CharField(max_length=100)
	
	


class vendor_product_tb(models.Model):
	productname=models.CharField(max_length=255)
	venid= models.ForeignKey(vendor_register_tb, on_delete=models.CASCADE)
	oldprice=models.CharField(max_length=255)
	newprice=models.CharField(max_length=255)
	desc=models.CharField(max_length=255)
	image=models.ImageField(upload_to="product/")
	catagory=models.CharField(max_length=255)
	qty=models.CharField(max_length=255)
	