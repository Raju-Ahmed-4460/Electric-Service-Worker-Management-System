from django.urls import path
from  eee .views import Userdashboard,Managerdashboard

urlpatterns = [

    path("userdashboard/",Userdashboard,name="userdashboard"),
    path("managerdashboard/",Managerdashboard,name="managerdashboard"),

    
]
