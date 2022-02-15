from rest_framework import routers
from knox import views as KnoxView
from django.urls import path
from .import views
router = routers.DefaultRouter()


app_name="product"

urlpatterns = [ 
    path('cat/<int:categoryId>/<str:action>',views.categoryView,name="categoryView"), 
    path('producttype/<int:productTypeId>/<str:action>',views.productTypeView,name="productTypeView"), 
    path('size/<int:sizeId>/<str:action>',views.sizeView,name="sizeView"),
    path('product/<int:productId>/<str:action>',views.productView,name="productView"), 
    path('badproduct/<int:badProductId>/<str:action>',views.badProductView,name="badProductView"),  
    path('returnedproduct/<int:returnedProductId>/<str:action>',views.returnedProductView,name="returnedProductView"),  

]
urlpatterns += router.urls