from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="credit_sales"

urlpatterns = [ 
    path('<int:customerID>/<str:action>',views.creditSalesView,name="creditSalesView"), 
    path('payment/<int:creditId>/<str:action>',views.paymentView,name="paymentView"), 
]
urlpatterns += router.urls