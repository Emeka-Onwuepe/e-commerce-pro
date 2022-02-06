from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="stock"

urlpatterns = [ 
    path('stock/<int:stockId>/<str:action>',views.stockView,name="stockView"), 

]
urlpatterns += router.urls