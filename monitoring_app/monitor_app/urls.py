from django.urls import path
from monitor_app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add_web', views.add_web, name="add_web"),
    path('website', views.websiteApi, name = "website"),
    path("register", views.register, name="register"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("login_view", views.login_view, name="login_view"),
]