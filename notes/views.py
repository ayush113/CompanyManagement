from django.shortcuts import render
from django.db import connection
from .utils import namedtuplefetchall



# Create your views here.
def notes(request):
    with connection.cursor() as curr:
        curr.execute("select * from reminder where id=%s",[request.user.id])
        reminders = namedtuplefetchall(curr)
    return render(request, 'notes/index.html', {'notes': reminders})
