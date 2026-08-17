from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("user.urls")),
    path("", include("eee.urls")),

    # Root URL → Public User Dashboard
    path("", redirect("userdashboard")),
]