from rest_framework import routers
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="logistics"

urlpatterns = [ 
    path('location/<int:locationId>/<str:action>',views.locationView,name="locationView"), 
    
]
urlpatterns += router.urls