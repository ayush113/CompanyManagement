from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.db import connection

from projects.utils import namedtuplefetchall

# Create your views here.
def landing(request):
    return render(request,'home/landing.html')

@login_required
def dashboard(request):
    with connection.cursor() as curr:
        curr.execute("SELECT * FROM reminder WHERE id = %s",[request.user.id])
        res = namedtuplefetchall(curr)
    return render(request,'home/dashboard.html',{'result': res})
