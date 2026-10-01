from django.contrib import admin
from django.urls import include, path

from dashboard import views


urlpatterns = [
    path(
        "django-admin/",
        admin.site.urls,
    ),

    path(
        "",
        views.user_dashboard,
        name="home",
    ),

    path(
        "",
        include("dashboard.urls"),
    ),
]