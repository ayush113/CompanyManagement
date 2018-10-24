from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from projects.models import Project
from django.db import connection
from .utils import namedtuplefetchall

@login_required
def projects(request):
    with connection.cursor() as curr:
        curr.execute("SELECT project.project_id,project_name,leader,customer_id,start_date,"
                     "deadline FROM project INNER JOIN works_on ON project.project_id=works_on.project_id "
                     "WHERE works_on.user_id=%s ",[request.user.id])
        res = namedtuplefetchall(curr)
        print(res[0].start_date)
    return render(request,'projects/index.html',{'projects':res})