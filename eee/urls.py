from django.urls import path
from  eee .views import Userdashboard

urlpatterns = [

    path("userdashboard/",Userdashboard,name="userdashboard"),

    
]
