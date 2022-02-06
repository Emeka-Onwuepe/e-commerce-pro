from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="preOrder"

urlpatterns = [ 
    path('preorder/<int:preOrderId>/<str:action>',views.preOrderView,name="preOrderView"), 

]
urlpatterns += router.urls