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
from django.views.decorators.csrf import csrf_exempt

from .utils import send_mail

from DBMS import settings

from passlib.hash import pbkdf2_sha256 as encrypto

# Create your views here.

@login_required
@csrf_exempt
def social(request):
    if request.method == "POST":
        data = request.POST
        project_id = int(json.loads(data.get('projid')))
        head = data.get('head')
        head = json.loads(head)
        subhead = json.loads(data.get('subh'))
        content = json.loads(data.get('cont'))
        obtained = json.loads(data.get('pass'))
        with connection.cursor() as curr:
            curr.execute("SELECT manager_id,customer_id FROM socialMedia where project_id=%s",[project_id])
            rec_id =  namedtuplefetchall(curr)
        manager_id = rec_id[0].manager_id
        customer_id = rec_id[0].customer_id
        print("SENDING")

        with connection.cursor() as curr:
            curr.execute("select contact from customer where customer_id = %s",[customer_id])
            email = namedtuplefetchall(curr)
        customer_email = email[0].contact

        # Rename the email field with customer_email to send to customers when we have actual data

        pwd = settings.EMAIL_HOST_PASSWORD
        if encrypto.verify(obtained,pwd) == True:
            #print("asjdhasd")
            send_mail(head,subhead+'\n'+content,'Gauri Baraskar','gauribaraskar812@gmail.com',settings.EMAIL_HOST_USER,obtained)
        else:
            messages.warning(request,"Wrong Password Entered")
        return JsonResponse(1,safe=False)

    else:
        with connection.cursor() as curr:
            curr.execute(
                "select project.project_id,project_name from works_on,project where user_id=%s and project.project_id=works_on.project_id",[request.user.id])
            res = namedtuplefetchall(curr)
        return render(request, 'social/index.html', {'social': res})






