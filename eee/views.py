from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your views here.
def Userdashboard(request):
    user=User.objects.all()
    return render(request,"Userdashborad.html",{"user":user})

def Managerdashboard(request):
    user=User.objects.all()
    return render(request,"managerdashboard.html",{"user":user})