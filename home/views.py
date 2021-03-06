from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.db import connection

from projects.utils import namedtuplefetchall

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime

# Create your views here.
def landing(request):
    return render(request,'home/landing.html')

@login_required
@csrf_exempt
def dashboard(request):
    if request.method =="POST":
        data = request.POST
        try:
            id = data.get('id')
            id= int(json.loads(id))
            with connection.cursor() as curr:
                curr.execute("DELETE FROM reminder WHERE `index` = %s",[id])

            return JsonResponse(1,safe=False)
        except:
            data = request.POST
            desc = json.loads(data.get('reminder'))

            if desc == '':
                messages.warning(request,message="Empty Reminder Cannot be added")
                return JsonResponse(1,safe=False)
            else:
                prior = json.loads(data.get('priority'))
                if prior == "High":
                    prior = 1
                else:
                    prior = 0
                with connection.cursor() as curr:
                    curr.execute("INSERT INTO reminder(id,description,priority) VALUES (%s,%s,%s)",
                                 [request.user.id, desc, prior])
                return JsonResponse(1, safe=False)
    else:
        with connection.cursor() as curr:
            curr.execute("SELECT * FROM reminder WHERE id = %s", [request.user.id])
            res = namedtuplefetchall(curr)
        now = datetime.now()
        day = now.strftime("%A")
        month = now.strftime("%B")
        crtime = now.strftime('%H:%M')
        date = now.date().day
        time = {
            'time': crtime,
            'day': day,
            'month': month,
            'date': date
        }
        return render(request, 'home/dashboard.html', {'result': res, 'time': time})
