from rest_framework import routers
from knox import views as KnoxView
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="product"

urlpatterns = [ 
    path('cat/<int:categoryId>/<str:action>',views.categoryView,name="categoryView"), 
    path('producttype/<int:productTypeId>/<str:action>',views.productTypeView,name="productTypeView"), 
    path('product/<int:productId>/<str:action>',views.productView,name="productView"),  

]
urlpatterns += router.urls