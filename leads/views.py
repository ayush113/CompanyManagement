from django.shortcuts import render

# Create your views here.
def leads(request):
    return render(request,'leads/index.html')