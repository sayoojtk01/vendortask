from django.urls import path
from . import views

urlpatterns=[
    
	path('',views.index),
    path('shop/',views.shop),
    path('single/',views.single),
    # path('checkout/',views.checkout),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),


   
    
 
    path('cart/',views.cart),
    path('addtocart/',views.addtocart),
    path('cart_update/',views.cart_update),
    path('cart_delete/',views.cart_remove),
    path('payment/',views.payment),
    

]