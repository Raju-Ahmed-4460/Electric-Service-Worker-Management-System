from django.urls import path
from user .views import registration,user_login,activate,user_logout,create_group,assign_role,home
urlpatterns = [
    path("registration/",registration,name="registration"),
    path("activate/<uid>/<token>/",activate),
    path("login/",user_login,name="login"),
    path("logout/",user_logout,name="logout"),
    path("home/",home,name="home"),
    path("create_group/",create_group,name="creategroup"),
    path("assign_group/<int:user_id>/",assign_role,name="assigngroup"),
    
]

