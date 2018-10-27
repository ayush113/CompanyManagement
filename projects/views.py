from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from projects.models import Project
from django.db import connection
from .utils import namedtuplefetchall
from django.http import JsonResponse
from django.contrib import messages
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
        data = request.POST
        id = json.loads(data.get('id'))
        id = int(id)
        action = json.loads(data.get('act'))
        print(action)
        projid = int(json.loads(data.get('projid')))

        if(action == "remove"):
            if id == request.user.id:
                messages.warning(request, "Can Not Remove Yourself")
                return JsonResponse(1, safe=False)
            with connection.cursor() as curr:
                curr.execute("DELETE FROM works_on WHERE user_id=%s AND project_id=%s",[id,projid])
        else:
            role = data.get('role')
            with connection.cursor() as curr:
                curr.execute("UPDATE works_on SET role = %s WHERE user_id = %s AND project_id=%s",[role,id,projid])
            print(data)


        return JsonResponse(1,safe=False)

    else :
        with connection.cursor() as curr:
            curr.execute("select project.leader from project,works_on where works_on.project_id=project.project_id and project.leader=works_on.user_id and works_on.user_id=%s and project.project_id=%s",[request.user.id,request.GET.get('project_id')])
            result = namedtuplefetchall(curr)
        if len(result) == 0:
            leader = 0
        else:
            leader = 1
        with connection.cursor() as curr:
            curr.execute("select * from project where project_id=%s", [request.GET.get('project_id')])
            res = namedtuplefetchall(curr)

        with connection.cursor() as curr:
            curr.execute("select first_name,last_name,role,works_on.user_id,auth_user.email from works_on,auth_user where works_on.user_id = auth_user.id and works_on.project_id=%s",[request.GET.get('project_id')])
            roles = namedtuplefetchall(curr)
        try:
            return render(request, 'projects/project.html', {'data': res[0],'roles':roles,'leader':leader})
        except:
            return render(request, 'projects/project.html')


