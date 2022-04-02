from rest_framework import routers
from django.urls import path

from .import views
router = routers.DefaultRouter()


app_name="sales"

urlpatterns = [ 
    path('',views.salesView,name="salesView"), 
    path('sale/<str:purchaseId>/<str:type>',views.saleView,name="saleView"), 
    path('<int:productTypeId>',views.salesProductView,name="salesProductView"),
    path('process',views.processSalesView,name="processSalesView"),
    path('<int:branchID>/<str:date>/analysis',views.salesAnalysisView,name="salesAnalysisView"),
    path('<str:start_date>/<str:end_date>/<int:branchID>/rangeanalysis',views.rangeSalesView,name="rangeSalesView"),

]
urlpatterns += router.urls