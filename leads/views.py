from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from projects.utils import namedtuplefetchall
import json
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib import messages
# Create your views here.

@login_required
@csrf_exempt
def leads(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        name = json.loads(name)
        customerID = data.get('customerID')
        customerID = int(json.loads(customerID))
        descript = data.get('descript')
        descript = json.loads(descript)
        cost = data.get('cost')
        cost = json.loads(cost)
        startdate = datetime.now().date()

        with connection.cursor() as curr:
            curr.execute("SELECT MAX(project_id) as maxim from project")
            res  = namedtuplefetchall(curr)

        newprojid  = res[0].maxim + 1

        with connection.cursor() as curr:
            curr.execute("INSERT INTO project(project_id,project_name,leader,customer_id,start_date,description,cost) VALUES (%s,%s,%s,%s,%s,%s,%s)",[newprojid,name,request.user.id,customerID,startdate,descript,cost])
            curr.execute("INSERT INTO works_on(user_id,project_id,role) VALUES( %s,%s,'Leader')",[request.user.id,newprojid])
            curr.execute("DELETE FROM leads where proposed_project_info = %s and customer_id = %s",[name,customerID])

        messages.info(request,message="New Project Added")

        return JsonResponse(1,safe=False)
    else:
        with connection.cursor() as curr:
            curr.execute(
                "select leads.customer_id,customer_name,proposed_project_info,time_required,cost,leads.info from customer,leads where point_of_contact=%s and leads.customer_id=customer.customer_id",
                [request.user.id])
            res = namedtuplefetchall(curr)
        return render(request, 'leads/index.html', {'leads': res})




# @login_required
# @csrf_exempt
# def editpage(request):
#     if request.method == "POST":
#         data = request.POST
#
#
#         print('sdfghj')
#
#         name = data.get('name')
#         name = json.loads(name)
#         customerID = data.get('customerID')
#         customerID = json.loads(customerID)
#         descript = data.get('descript')
#         descript = json.loads(descript)
#         cost = data.get('cost')
#         cost = json.loads(cost)
#
#         print(name)
#
#         return JsonResponse(1, safe=False)
