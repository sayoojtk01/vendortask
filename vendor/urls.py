from django.urls import path
from . import views

urlpatterns=[
    
	path('',views.vindex),
    path('venregister/',views.register),
    path('venlogin/',views.login),
    path('venlogout/',views.logout),
    path('addproduct/',views.addproduct),
    path('prdelete/',views.prdelete),

]