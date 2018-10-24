from django.shortcuts import render

# Create your views here.
def social(request):
    return render(request,'social/index.html')
