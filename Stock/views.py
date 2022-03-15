from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Branch.models import Branch
from Product.models import Product, Size
from Stock.form import StockEditForm

from Stock.models import Stock

# Create your views here.

  
def stockView(request,stockId,branchId,action):
    
    branch = Branch.objects.get(pk=branchId)
    
    if stockId != 0:   
        stock_instance = Stock.objects.get(id=stockId)
    
    if request.method == "POST" and action == "add":
        data= request.POST
        product_size = data['product'].split("-")
        if len(product_size)>1:
            productId,sizeId = product_size
            product = Product.objects.get(pk=int(productId))
            size = Size.objects.get(pk = int(sizeId))
            Stock.objects.create(product=product,branch=branch,
                                 size=size,qty=int(data['qty']))
        else:
            product = Product.objects.get(pk=int(product_size))
            Stock.objects.create(product=product,branch=branch,
                                 size=int(size),qty=int(data['qty']))
        
        return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0,'branchId':branch.id}))
       
            
    if action == "edit":
        if request.method == "POST":
            form = StockEditForm(data= request.POST,instance=stock_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('stock:stockView',
                        kwargs={"action":"view","stockId":0,'branchId':branch.id}))
            else:
                return render(request,"stock/stock.html",
                  {"form":form,"stockId":stock_instance.id,
                   "action":"edit",'branch':branch,"instance":stock_instance})
        else:
            return render(request,"stock/stock.html",
                  {"form":StockEditForm(instance=stock_instance),
                   "stockId":stock_instance.id,"action":"edit",
                   "instance":stock_instance,'branch':branch})
    
    if action == "delete":
        stock_instance.delete()
        return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0,'branchId':branch.id}))
                 
    return render(request,"stock/stock.html",
                  {"stockId":0,"action":"add",'branch':branch})