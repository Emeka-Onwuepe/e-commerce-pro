from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="frontview"

urlpatterns = [
    
    path('',views.homeView,name="homeView"), 
    path('category/<int:catId>',views.categoryView,name="categoryView"),
    path('cart',views.cartView,name="cartView"),  
    
   
      

]
urlpatterns += router.urls