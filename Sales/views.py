from django.shortcuts import render

from Product.models import Product
from Sales.form import salesForm

# Create your views here.
def salesView(request):
    return render(request,"sales/sales.html")

def salesProductView(request,productTypeId):
    products = Product.objects.filter(product_type = productTypeId,
                                      branches=request.user.branch)
    print(products)
    return render(request,"sales/product.html",{"products":products,"form":salesForm})