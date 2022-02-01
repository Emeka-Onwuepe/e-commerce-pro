from rest_framework import routers
from knox import views as KnoxView
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="branch"

urlpatterns = [
    
    # path('<str:action>',views.branchView,name="branchView"), 
    path('<int:branchId>/<str:action>',views.branchView,name="branchView"), 
    # path('branchproduct/<int:branchProductId>/<str:action>',views.branchProductView,name="branchProductView"), 
    # path('<int:branchId>/returned',views.branchDetailsView,name="returned"),
      

]
urlpatterns += router.urls