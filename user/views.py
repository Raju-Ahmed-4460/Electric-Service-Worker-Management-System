from django.shortcuts import render, redirect
from user.forms import RegistrationForm,login_form
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse


User=get_user_model()


def registration(request):
    form=RegistrationForm()

    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)

            user.set_password(form.cleaned_data.get('password'))

            user.is_active=False

            user.save()
            return redirect("registration")
    

    return render(request,"registration.html",{'form':form})

def activate(request,uid,token):

    try:
        uid=urlsafe_base64_decode(uid).decode()
        user=User.objects.get(pk=uid)
    except:
        user=None
    
    if user and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect("login")
    
    return HttpResponse ("this is invalid link")


def user_login(request):
    form=login_form()

    if request.method=="POST":
        form=login_form(request.POST)

        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect("home")
            
    
    return render(request,"login.html",{'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,"home.html")


