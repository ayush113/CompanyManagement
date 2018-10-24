from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def leads(request):
    return render(request,'leads/index.html')