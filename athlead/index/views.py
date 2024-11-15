from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as l,logout
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')
@login_required(login_url='login')
def workout(request):
    return render(request, 'workout.html')
@login_required(login_url='login')
def diet(request):
    return render(request, 'diet.html')
@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            l(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render (request,'signup.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def caltrack(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(
            api_url + query, headers={'X-Api-Key': 'Uvm6RKpxilr4R6bPdguZcA==Tdel55IQ5xEMYVtY'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'caltrack.html', {'api': api})
    else:
        return render(request, 'caltrack.html', {'query': 'Enter a valid query'})

@login_required(login_url='login')
def error_page(request):
    return render(request,'error.html')
