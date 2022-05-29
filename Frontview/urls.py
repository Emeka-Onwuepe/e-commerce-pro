from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="frontview"

urlpatterns = [
    
    path('',views.homeView,name="homeView"), 
    path('cart',views.cartView,name="cartView"), 
    path('csales', views.customerOrderHistoryView, name="csales"),
    path('processorder',views.processPaymentView,name="processPaymentView"), 
    path('category/<str:cat>',views.categoryView,name="categoryView"),
    path('details/<str:purchaseId>',views.saleView,name="saledetailsView"),
    
   
      

]
urlpatterns += router.urls