from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="sales"

urlpatterns = [ 
    path('',views.salesView,name="salesView"), 
    path('sale/<str:purchaseId>',views.saleView,name="saleView"), 
    path('<int:productTypeId>',views.salesProductView,name="salesProductView"),
    path('process',views.processSalesView,name="processSalesView"),


]
urlpatterns += router.urls