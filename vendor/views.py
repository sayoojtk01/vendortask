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
        street = request.POST['street']
        street2 = request.POST['street2']
        city = request.POST['city']
        state = request.POST['state']
        pin = request.POST['pin']
        phone = request.POST['phone']
        
        
        if password != cpassword:
            return render(request, "vendor/register.html", {"error": "Passwords don't match!"})
        
      
        check = vendor_register_tb.objects.filter(email=email)
        if check:
            return render(request, 'vendor/register.html', {"error": "Email has already been taken!"})
        
        
        razorpay_payloads = {
              
            "email":email,
            "phone":phone,
            "type":"route",
            "legal_business_name":"downy shoe",
            "business_type":"partnership",
            "contact_name":name,
            "profile":{
                "category":"ecommerce",
                "subcategory":"ecommerce_marketplace",
                "addresses":{
                    "registered":{
                        "street1":street,
                        "street2":street2,
                        "city":city,
                        "state":state,
                        "postal_code":pin,
                        "country":"IN"
                    }
                }
            }
            
            }


        razorpay_response = requests.post('https://api.razorpay.com/v2/accounts', json=razorpay_payloads, auth=('rzp_test_9wyCq1vo5Rar4X', 'NVnQDSzoPqNaWP5Ka8d4zqGF'))


        
        
        if razorpay_response.status_code == 200:


            user = vendor_register_tb(name=name, email=email, password=password, bank=bank, ifsc=ifsc)
            user.save()
            return render(request, 'vendor/login.html', {"error": "Registered successfully. Please login!"})
        else:
            
            return render(request, 'vendor/register.html', {"error": "Failed to create account."})
    
    else:
        return render(request, 'vendor/register.html',{"error": "nooooooooooo"})
    




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



