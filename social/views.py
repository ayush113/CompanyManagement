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


# Create your views here.

@login_required
def social(request):
    with connection.cursor() as curr:
        curr.execute("select project.project_id,project_name from works_on,project where user_id=6 and project.project_id=works_on.project_id")
        res = namedtuplefetchall(curr)
    return render(request,'social/index.html',{'social':res})


