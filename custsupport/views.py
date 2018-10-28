from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from projects.utils import namedtuplefetchall
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.

@login_required
@csrf_exempt
def cust(request):

    printtag = request.GET.get('printtag')
    custid = request.GET.get('custid')

    if printtag is None or printtag == 0:
        res2 = {'data':'isNone'}
    elif int(printtag) == 1:
        custid = int(custid)
        with connection.cursor() as curr:
            curr.execute("SELECT complaints from customer where customer_id = %s",[custid])
            res2 = namedtuplefetchall(curr)
    elif int(printtag) == 2:
        custid = int(custid)
        with connection.cursor() as curr:
            curr.execute("SELECT * from bills where customer_id=%s",[custid])
            res2 = namedtuplefetchall(curr)
    elif int(printtag) == 3:
        custid = int(custid)
        with connection.cursor() as curr:
            curr.execute("SELECT changes from customer where customer_id = %s",[custid])
            res2 = namedtuplefetchall(curr)


    # printtag = 0
    #
    # """
    # printtag = 1 implies return complaints
    # printtag = 2 implies return bills
    # printtag = 3 implies return changes
    #
    # """
    # res2 = {'none':'no data'}
    #
    # if request.method== "POST":
    #     data = request.POST
    #     printtag = int(json.loads(data.get('printtag')))
    #     custid = int(json.loads(data.get('custid')))
    #     if printtag == 1:
    #         with connection.cursor() as curr:
    #             curr.execute("SELECT complaints from customer where customer_id = %s",[custid])
    #             res2 = namedtuplefetchall(curr)
    #     elif printtag == 2:
    #         with connection.cursor() as curr:
    #             curr.execute("SELECT * from bills where customer_id=%s",[custid])
    #             res2 = namedtuplefetchall(curr)
    #     elif printtag == 3:
    #         with connection.cursor() as curr:
    #             curr.execute("SELECT changes from customer where customer_id = %s")
    #             res2 = namedtuplefetchall(curr)
    #
    with connection.cursor() as curr:
        curr.execute("SELECT * FROM customer WHERE point_of_contact=%s", [request.user.id])
        res = namedtuplefetchall(curr)
    return render(request,'custsupport/index.html',{'customer':res,'printtag':printtag,'data':res2})


