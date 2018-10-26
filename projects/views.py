from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from projects.models import Project
from django.db import connection
from .utils import namedtuplefetchall
from django.http import JsonResponse
import json

@login_required
def projects(request):
    with connection.cursor() as curr:
        curr.execute("select first_name,last_name,q1.project_id,project_name,leader,customer_id,start_date,deadline from auth_user,(SELECT project.project_id,project_name,leader,customer_id,start_date,deadline FROM project INNER JOIN works_on ON project.project_id=works_on.project_id WHERE works_on.user_id=%s) as q1 where q1.leader = auth_user.id",[request.user.id])
        res = namedtuplefetchall(curr)
    return render(request,'projects/index.html',{'projects':res})

@login_required
@csrf_exempt
def editpage(request):
    variable = 0
    if request.method == "POST":
        print("HERE")
        data = request.POST
        print(data)
        stuff = data.get('name')
        id = data.get('id')
        id = json.loads(id)
        id = int(id)
        stuff = json.loads(stuff)
        with connection.cursor() as curr:
            print(request.GET.get('project_id'))
            curr.execute("UPDATE project SET project_name=%s WHERE project_id=%s",[stuff,id])
        return JsonResponse(variable,safe=False)

    else :
        with connection.cursor() as curr:
            curr.execute("select * from project where project_id=%s", [request.GET.get('project_id')])
            res = namedtuplefetchall(curr)

        with connection.cursor() as curr:
            curr.execute("select first_name,last_name,role from works_on,auth_user where works_on.user_id = auth_user.id and works_on.project_id=%s",[request.GET.get('project_id')])
            roles = namedtuplefetchall(curr)
        try:
            return render(request, 'projects/project.html', {'data': res[0],'roles':roles})
        except:
            return render(request, 'projects/project.html')


