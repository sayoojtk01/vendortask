from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from.models import *
from vendor.models import*
import os
import razorpay
from django.conf import settings
from django.http import JsonResponse
import json



import requests


# Create your views here.

def index(request):
	
	return render(request,'index.html')


def single(request):
	pid=request.GET['pid']
	query=vendor_product_tb.objects.filter(id=pid)
	return render(request,'single.html',{"data":query})

# def checkout(request):
# 	return render(request,'cart.html')

def login(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		check=user_register_tb.objects.filter(email=email,password=password)
		if check:
			for x in check:
				request.session['uid']=x.id
				request.session['uname']=x.username
				return render(request,'index.html',{"success":"Logged  In"})
		else:
			return render(request,'login.html',{"error":"Invalid Data Please Register"})
	else:
		return render(request,'login.html')
	

def register(request):
	if request.method=='POST':
		name=request.POST['name']
		email=request.POST['email']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		phone=request.POST['phone']
		check=user_register_tb.objects.filter(email=email)
		if password==cpassword:
			if check:
				return render(request,'register.html',{"error":"email has already taken !"})
			else:
				user=user_register_tb(username=name,email=email,password=password,phone=phone)
				user.save()
				return render(request,'login.html',{"error":"Rgisterd sucessfully Please Login  !"})
		else:
			return render(request,"register.html",{"error":"Passwords doesn't match !"})
	else:
		return render(request,'register.html')
	



def logout(request):
	if request.session.has_key('uid'):
		del request.session['uid']
		del request.session['uname']
		return  HttpResponseRedirect('/')
	else:
		return redirect('/')
	




	


def shop(request):
	query=vendor_product_tb.objects.all()
	return render(request,'shop.html',{"data":query})







# --------------------OLD ADD TO CART----------------

def addtocart(request):
	if request.session.has_key('uid'):
		if request.method == 'POST':

			pid = request.GET['pid']
			prd = vendor_product_tb.objects.get(id=pid)

			uid=request.session['uid']
			usr=user_register_tb.objects.get(id=uid)

			product=vendor_product_tb.objects.filter(id=pid)
			for x in product:
				price=x.newprice
			total=0
			total=float(price)


			data1=cart_tb.objects.filter(uid=usr,pid=prd,status="pending")
			if data1:
				total1=0
				for x in data1:
					qty=int(x.quantity)
					qty+=1
					price=x.pid.newprice
					price1=x.total
					total1=total1+float(price1)


				total=0
				total=(float(price)*int(qty))
				add=cart_tb.objects.filter(uid=usr,pid=prd,status="pending").update(total=total,quantity=qty)
				datas=cart_tb.objects.filter(uid=usr,status="pending")
				grtotal=0
				for x in datas:
					price=float(x.total)
					
					grtotal=grtotal+price
				
				return render(request,"cart.html",{"data":datas,"total":grtotal})
			
			else:
				add=cart_tb(pid=prd,uid=usr,quantity=1,total=total)
				add.save()

			datas=cart_tb.objects.filter(uid=usr,status="pending")
			total = 0
			for x in datas:
				price=x.total
				total=total+float(price)
			return render(request, "cart.html",{"data":datas,"total":total})
		
		else:
			pid=request.GET['pid']
			datas=vendor_product_tb.objects.filter(id=pid)
			return render(request,"cart.html",{"data":datas})
	
	else:
		return HttpResponseRedirect("/login/")
  
            
       
    



	
# def addtocart(request):
#     if request.session.has_key('uid'):
#         if request.method == "POST":
#             pid=request.GET["pid"]
#             prd=vendor_product_tb.objects.get(id=pid)
#             uid=request.session['uid']
#             usr=user_register_tb.objects.get(id=uid)
#             product=vendor_product_tb.objects.filter(id=pid)
#             for x in product:
#                 price=x.newprice
#             deliv=(int(price)*10)/100
#             total=0
#             total=int(deliv)+int(price)


#             data1=cart_tb.objects.filter(uid=usr,pid=prd,status="pending")
#             if data1:
#                 total1=0
#                 for x in data1:
#                     qty=int(x.quantity)
#                     qty+=1
#                     price=x.pid.newprice
#                     price1=x.total
#                     total1=total1+float(price1)

			

#                 # add=cart_tb.objects.filter(uid=usr,pid=prd,status="pending").update(quantity=qty)
#                 total=0
#                 # for x in data1:
#                 # deliv=(float(price)*10)/100
#                 total=(float(price)*int(qty))
#                 add=cart_tb.objects.filter(uid=usr,pid=prd,status="pending").update(total=total,quantity=qty)
#                 datas=cart_tb.objects.filter(uid=usr,status="pending")
	
                

#                 return render(request,"cart.html",{"data":datas,"total":total1})
#             else:
#                 add=cart_tb(pid=prd,uid=usr,quantity=1,total=total)
#                 add.save()
#             datas=cart_tb.objects.filter(uid=usr,status="pending")
#             total=0
#             for x in datas:
#                 price=x.total
#                 total=total+float(price)
#             return render(request,"cart.html",{"data":datas,"total":total})
#         else:
#             pid=request.GET['pid']
#             datas=vendor_product_tb.objects.filter(id=pid)
#             return render(request,"cart.html",{"data":datas})
#     else:
#         return HttpResponseRedirect("/login/")







def cart(request):
    # mydata=cart_tb.objects.all()
    # return render(request,"cart.html",{"data1":mydata})
    uid=request.session['uid']
    usr=user_register_tb.objects.get(id=uid)
    datas=cart_tb.objects.filter(uid=usr,status="pending")
    total=0
    for x in datas:
        price=x.total
        total=total+float(price)
    return render(request,"cart.html",{"data":datas,"total":total})
   


def cart_update(request):
	cid=request.GET['cid']
	quantity=request.POST['qty']
	cart=cart_tb.objects.filter(id=cid)
	for x in cart:
		price=x.pid.newprice
		qty=x.quantity
		quantity1=x.pid.qty
		pid=x.pid.id

	newprice=(float(price)*int(quantity))
	cart_tb.objects.filter(id=cid).update(quantity=quantity,total=newprice)
	lessqty=int(quantity1)-int(qty)
	vendor_product_tb.objects.filter(id=pid).update(qty=lessqty)
	return HttpResponseRedirect("/cart/")
	


def cart_remove(request):
    cid=request.GET['cid']
    cart_tb.objects.filter(id=cid).delete()
    return HttpResponseRedirect("/cart/")





# def payment(request):
# 	return render(request,'payment.html')




# def payment(request):
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#     # Calculate amounts for the parties involved
#     total_amount = 1000  # Example amount in paise
#     third_party_amount = 700
#     your_amount = total_amount - third_party_amount

#     # Create a Razorpay order
#     order_data = {
#         'amount': total_amount,
#         'currency': 'INR',
#         'payment_capture': 1  # Auto-capture payments
#     }
#     order = client.order.create(data=order_data)

#     # Set up the Route for split payments
#     route_data = {
#         'order_id': order['id'],
#         'splits': [
#             {
#                 'linked_account_id': '5478456555887',
#                 'amount': third_party_amount,
#             },
#             {
#                 'linked_account_id': '4578699455112',
#                 'amount': your_amount,
#             }
#         ]
#     }
#     route = client.route.create(data=route_data)

#     # Return the route ID to your frontend for payment processing
#     return JsonResponse({'route_id': route['id']})


# 2222222222222222

# def payment(request):
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#     # Calculate amounts for the parties involved
#     total_amount = 1000  # Example amount in paise
#     third_party_amount = 700
#     your_amount = total_amount - third_party_amount

#     # Create a Razorpay order
#     order_data = {
#         'amount': total_amount,
#         'currency': 'INR',
#         'payment_capture': 1  # Auto-capture payments
#     }
#     order = client.order.create(data=order_data)

#     # Set up the order's notes to include split details
#     order_notes = {
#         'split_details': [
#             {
#                 'linked_account_id': '5487571456699',
#                 'amount': third_party_amount,
#             },
#             {
#                 'linked_account_id': '4578865428475',
#                 'amount': your_amount,
#             }
#         ]
#     }
#     client.order.edit_order(order['id'], notes=order_notes)

#     # Return the order ID to your frontend for payment processing
#     return JsonResponse({'order_id': order['id']})


# 33333333333333333333



# def payment(request):
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#     # Calculate amounts for the parties involved
#     total_amount = 1000  # Example amount in paise
#     third_party_amount = 700
#     your_amount = total_amount - third_party_amount

#     # Create a Razorpay order
#     order_data = {
#         'amount': total_amount,
#         'currency': 'INR',
#         'payment_capture': 1,  # Auto-capture payments
#         'notes': {
#             'split_details': [
#                 {
#                     'linked_account_id': '7874577886',
#                     'amount': third_party_amount,
#                 },
#                 {
#                     'linked_account_id': '455589665544',
#                     'amount': your_amount,
#                 }
#             ]
#         }
#     }
#     order = client.order.create(data=order_data)

#     # Return the order ID to your frontend for payment processing
#     return JsonResponse({'order_id': order['id']})


# 44444444444444444444444444


def payment(request):
		if request.session.has_key('uid'):
			uid=request.session['uid']
			
			client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

			data = json.loads(request.body)
			total_amount = data.get('total')
			cart_id=data.get('product_id')

			


			ven_data=cart_tb.objects.filter(id=cart_id)
			
			for x in ven_data:
				vname=x.pid.venid.name
				ven_bank=x.pid.venid.bank
				ifsc=x.pid.venid.ifsc
			
			
				
			vendor_amount = int(total_amount) * 0.7 
			your_amount = total_amount - vendor_amount

			
			split_details = [
				{
					'linked_account_id': ven_bank,
					'amount': vendor_amount,
				},
				{
					'linked_account_id': '888888888888888',
					'amount': your_amount,
				}
			]

			
			split_details_json = json.dumps(split_details)
			print(split_details)






			order_data = {
				'amount': total_amount,
				'currency': 'INR',
				'payment_capture': 1,  
				'notes': {
					'split_details': split_details_json,
				}
			}
			order = client.order.create(data=order_data)

			order_amount = total_amount * 100  

			return JsonResponse({'order_id': order['id'], 'order_amount': order_amount})
		








