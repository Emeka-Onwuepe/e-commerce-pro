from django.http import JsonResponse
from django.shortcuts import render
import json

from Product.models import Product
from Sales.form import salesForm
from Sales.models import Items, Sales
from User.Forms import CustomerForm

# Create your views here.
def salesView(request):
    return render(request,"sales/sales.html")

def saleView(request,purchaseId):
    sale = Sales.objects.get(purchase_id= purchaseId)
    return render(request,"sales/sale.html",{"sale":sale})

def salesProductView(request,productTypeId):
    products = []
    initial = True
    if productTypeId != 0:
        initial = False
        products = Product.objects.filter(product_type = productTypeId,
                                      branches=request.user.branch)
    return render(request,"sales/product.html",{"products":products,"customerForm":CustomerForm,
                                                "saleForm":salesForm,'initial':initial})


def processSalesView(request):
   if request.method == "POST":
       data = json.loads(request.body.decode("utf-8"))
       orderlist = data['orders']
       del data['orders']
       
       sales = Sales.objects.create(branch=request.user.branch,channel ="store",**data)
       print(sales)
       for item in orderlist:
            product = Product.objects.get(pk=int(item['id']))
            Item =  Items.objects.create(product=product,product_type=item['product_type'],
                                    size=item['size'],color=item['color'],qty=item['qty'],
                                    unit_price=item['price'],total_price=item['productTotal'])
            sales.items.add(Item)
         
           
       return JsonResponse({"data":sales.purchase_id})