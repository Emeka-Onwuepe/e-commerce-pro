from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Pre_Order.form import PreOrderForm
from Pre_Order.models import Pre_Order

# Create your views here.

def preOrderView(request,preOrderId,action):
    
    preorders = None
    if action == "view":
        preorders = Pre_Order.objects.filter(archive=False)
    elif action == "getarchive":
        preorders = Pre_Order.objects.filter(archive=True)
           
    if preOrderId != 0:   
        pre_order_instance = Pre_Order.objects.get(id=preOrderId)
        
    if action == "archive":
        pre_order_instance.archive = True
        pre_order_instance.save()
        return HttpResponseRedirect(reverse('preOrder:preOrderView',
            kwargs={"action":"view","preOrderId":0}))
        
    if request.method == "POST" and action == "add":
        form = PreOrderForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('preOrder:preOrderView',
            kwargs={"action":"view","preOrderId":0}))
        else:
            return render(request,"Pre_Order/preOrder.html",
                  {"form":form,"preOrderId":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = PreOrderForm(data= request.POST,instance=pre_order_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('preOrder:preOrderView',
                        kwargs={"action":"view","preOrderId":0}))
            else:
                return render(request,"Pre_Order/preOrder.html",
                  {"form":form,"preOrderId":pre_order_instance.id,"action":"edit",
                   "preorders":preorders})
        else:
            return render(request,"Pre_Order/preOrder.html",
                  {"form":PreOrderForm(instance=pre_order_instance),
                   "preOrderId":pre_order_instance.id,"action":"edit",
                   "preorders":preorders})
    
    if action == "delete":
        pre_order_instance.delete()
        return HttpResponseRedirect(reverse('preOrder:preOrderView',
            kwargs={"action":"view","preOrderId":0}))
                 
    return render(request,"Pre_Order/preOrder.html",
                  {"form":PreOrderForm(),"preOrderId":0,"action":"add","preorders":preorders})