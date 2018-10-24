from django.shortcuts import render

# Create your views here.
def cust(request):
    return render(request,'custsupport/index.html')