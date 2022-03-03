from django.urls import path
from .import views


app_name="user"

urlpatterns = [
    path('login/',views.loginView,name="loginView"),
    path('login/<path:next>',views.loginView,name="loginRedirect"),
    path('logout',views.logoutView,name="logoutView"), 
    # path('<str:fullname>/dashboardView',views.dashboardView,name="dashboardView"),  
    path('user/<int:userId>/<str:action>',views.userView,name="userView"), 
    path('customer/<int:customerId>/<str:action>',views.customerView,name="customerView"),

]