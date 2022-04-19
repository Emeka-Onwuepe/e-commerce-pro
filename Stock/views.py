from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Branch.models import Branch, Branch_Product
from Product.models import Product, Size
from Stock.form import StockEditForm

from Stock.models import Stock

# Create your views here.

@login_required(login_url="user:loginView")
def stockView(request,stockId,branchId,action):
    
    branch = Branch.objects.get(pk=branchId)
    
    stock_list = []
    
    for product in branch.products_branches.all():
        dic = {}
        if product.size:
            for size in product.multipleSIzes.all():
                dic["product"] = product
                dic['size'] = size
                stocks = Stock.objects.filter(product=product.id,
                                              branch = branch.id,
                                              size_instance = size.id)[0:1]
                if stocks:         
                    dic['stock'] = stocks
                    stock_list.append(dic)
                dic = {}
        else:
            dic["product"] = product
            dic['size'] = None
            stocks = Stock.objects.filter(product=product.id,
                                              branch = branch.id)[0:1]
            
            if stocks:
                dic['stock'] = stocks
                stock_list.append(dic)  
            
            dic = {}
            
    
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
                                 size_instance=size,qty=int(data['qty']))
        else:
            product = Product.objects.get(pk=int(data['product']))
            Stock.objects.create(product=product,branch=branch,qty=int(data['qty']))
        
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
                   "action":"edit",'branch':branch,"instance":stock_instance,
                   "stock_list":stock_list})
        else:
            return render(request,"stock/stock.html",
                  {"form":StockEditForm(instance=stock_instance),
                   "stockId":stock_instance.id,"action":"edit",
                   "instance":stock_instance,'branch':branch,
                   "stock_list":stock_list})
    
    if action == "delete":
        stock_instance.delete()
        return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0,'branchId':branch.id}))
                 
    return render(request,"stock/stock.html",
                  {"stockId":0,"action":"add",'branch':branch,
                   "stock_list":stock_list})