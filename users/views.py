from django.shortcuts import render

from . import models

# Create your views here.

def login(request):
    if request.method=='POST':
        print("AYUSH")
    return render(request,'users/login.html')


def signUp(request):
    if (request.method == "POST"):
        data = request.POST
        password = data.get('password')
        email = data.get('email')
        repassword =  data.get('repassword')
        password = json.loads(password)
        email = json.loads(email)
        obj = Users(username=uname, password=password, email=email)
        obj.save()
        someuser = authuser.objects.create_user(uname,email,password)
        someuser.save()
        #results = '1'
        return redirect(reverse('login'))
        #return JsonResponse(results, safe=False)
    else:
        return render(request, 'users/signup.html')


    return render(request,'users/signUp.html')