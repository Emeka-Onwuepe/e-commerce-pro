from django.urls import path
from .import views


app_name="user"

urlpatterns = [
    path('',views.loginView,name="loginView"),
    path('logout',views.logoutView,name="logoutView"), 
    path('<str:fullname>/dashboardView',views.dashboardView,name="dashboardView"),  

]