from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from projects.utils import namedtuplefetchall

# Create your views here.

@login_required
def cust(request):
    with connection.cursor() as curr:
        curr.execute("SELECT * FROM customer WHERE point_of_contact=%s",[request.user.id])
        res = namedtuplefetchall(curr)
    return render(request,'custsupport/index.html',{'customer':res})