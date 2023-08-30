from django.shortcuts import render,redirect
from vapp.models import*
from vendor.models import*
from django.http import HttpResponseRedirect
import razorpay
import requests

# Create your views here.


def vindex(request):
    if request.session.has_key('vid'):
        venid=request.session['vid']
        query=vendor_product_tb.objects.filter(venid=venid)
        return render(request,'vendor/index.html',{"data":query})
    else:
          return redirect('/vendor/venlogin/')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        bank = request.POST['account_number']
        ifsc = request.POST['ifsc_code']
        
        # Check if passwords match
        if password != cpassword:
            return render(request, "vendor/register.html", {"error": "Passwords don't match!"})
        
        # Check if the email is already taken
        check = vendor_register_tb.objects.filter(email=email)
        if check:
            return render(request, 'vendor/register.html', {"error": "Email has already been taken!"})
        
        # Create a Razorpay customer account
        razorpay_payload = {
            "name": name,
            "email": email,
            # Add any other relevant fields for customer creation
        }
        razorpay_response = requests.post('https://api.razorpay.com/v1/customers', json=razorpay_payload, auth=('rzp_test_9wyCq1vo5Rar4X', 'NVnQDSzoPqNaWP5Ka8d4zqGF'))
        
        if razorpay_response.status_code == 200:
            # Customer account created successfully, proceed with saving user data
            user = vendor_register_tb(name=name, email=email, password=password, bank=bank, ifsc=ifsc)
            user.save()
            return render(request, 'vendor/login.html', {"error": "Registered successfully. Please login!"})
        else:
            # Handle Razorpay customer creation failure
            return render(request, 'vendor/register.html', {"error": "Failed to create account."})
    
    else:
        return render(request, 'vendor/register.html')
    




def login(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		check=vendor_register_tb.objects.filter(email=email,password=password)
		if check:
			for x in check:
				request.session['vid']=x.id
				request.session['vname']=x.name
				return render(request,'vendor/index.html',{"success":"Logged  In"})
		else:
			return render(request,'vendor/login.html',{"error":"Invalid Data Please Register"})
	else:
              return render(request,'vendor/login.html')


def logout(request):
	if request.session.has_key('vid'):
		del request.session['vid']
		del request.session['vname']
		return  HttpResponseRedirect('/')
	else:
		return redirect('/')






def addproduct(request):
    if request.session.has_key('vid'):
        if request.method=='POST':
            name=request.POST['name']
            price=request.POST['price']
            desc=request.POST['desc']
            qty=request.POST['qty']
            image=request.FILES['image']
            category=request.POST['category']

            venid=request.session['vid']
            vendor=vendor_register_tb.objects.get(id=venid)

            user=vendor_product_tb(productname=name,newprice=price,desc=desc,qty=qty,image=image,catagory=category,venid=vendor)
            user.save()
            return redirect('/vendor/')
        else:
            return render(request,'vendor/productadd.html')
    else:
          return redirect('/vendor/venlogin/')
	


def prdelete(request):
	regid=request.GET['regid']
	data=vendor_product_tb.objects.filter(id=regid).delete()
	return redirect('/vendor/')



