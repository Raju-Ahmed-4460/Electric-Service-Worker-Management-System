from django.urls import path
from user .views import registration,user_login,activate,user_logout,home
urlpatterns = [
    path("registration/",registration,name="registration"),
    path("activate/<uid>/<token>/",activate),
    path("login/",user_login,name="login"),
    path("logout/",user_logout,name="logout"),
    path("home",home,name="home"),
    
]

