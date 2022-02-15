from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="sales"

urlpatterns = [ 
    path('',views.salesView,name="salesView"), 
    path('<int:productTypeId>',views.salesProductView,name="salesProductView"),

]
urlpatterns += router.urls