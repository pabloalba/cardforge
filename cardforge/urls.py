from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .designer import views as designer_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("social_django.urls", namespace="social")),

    path("login", auth_views.login, name="login"),
    path("logout", designer_views.logout, name="logout"),
    path("login/success", designer_views.login_success, name="login_success"),

    path("", designer_views.home, name="home"),
    path("api/me", designer_views.MeDetail.as_view(), name="me"),
    path("api/games", designer_views.GameList.as_view()),
    path("api/games/<int:pk>", designer_views.GameDetail.as_view()),
    path("api/games/<int:pk>/owners", designer_views.GameOwners.as_view()),
]
