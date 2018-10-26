from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from projects.utils import namedtuplefetchall

# Create your views here.

@login_required
def leads(request):
    with connection.cursor() as curr:
        curr.execute("select customer_name,proposed_project_info,time_required,cost from customer,leads where point_of_contact=%s and leads.customer_id=customer.customer_id",[request.user.id])
        res = namedtuplefetchall(curr)
    return render(request,'leads/index.html',{'leads':res})