from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="credit_sales"

urlpatterns = [ 
    path('',views.creditSalesView,name="creditSalesView"), 
]
urlpatterns += router.urls