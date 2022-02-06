from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Branch.models import Branch
from Stock.form import StockEditForm, StockForm

from Stock.models import Stock

# Create your views here.

  
def stockView(request,stockId,action):
  
    if stockId != 0:   
        stock_instance = Stock.objects.get(id=stockId)
    
    if request.method == "POST" and action == "add":
        form = StockForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0}))
        else:
            return render(request,"stock/stock.html",
                  {"form":form,"stockId":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = StockEditForm(data= request.POST,instance=stock_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('stock:stockView',
                        kwargs={"action":"view","stockId":0}))
            else:
                return render(request,"stock/stock.html",
                  {"form":form,"stockId":stock_instance.id,"action":"edit","instance":stock_instance})
        else:
            return render(request,"stock/stock.html",
                  {"form":StockEditForm(instance=stock_instance),
                   "stockId":stock_instance.id,"action":"edit","instance":stock_instance})
    
    if action == "delete":
        stock_instance.delete()
        return HttpResponseRedirect(reverse('stock:stockView',
            kwargs={"action":"view","stockId":0}))
                 
    return render(request,"stock/stock.html",
                  {"form":StockForm(),"stockId":0,"action":"add"})