from django.contrib import admin
from django.urls import path, include
from eee.views import Userdashboard


urlpatterns = [
    path("", Userdashboard.as_view(), name="root"),

    path("admin/", admin.site.urls),

    path("", include("user.urls")),
    path("", include("eee.urls")),
]