from django.urls import path

from . import views

urlpatterns=[
    path('',views.cust,name='customer'),
    path('bills/',views.bills,name='bills')

]