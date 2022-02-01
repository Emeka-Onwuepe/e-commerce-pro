from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Branch.forms import BranchForm
from Branch.models import Branch

# Create your views here.

def branchView(request,branchId,action):
  
    if branchId != 0:   
        branch_instance = Branch.objects.get(id=branchId)
    
    if request.method == "POST" and action == "add":
        form = BranchForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('branch:branchView',
            kwargs={"action":"view","branchId":0}))
        else:
            return render(request,"branch/branch.html",
                  {"form":form,"branchID":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = BranchForm(data= request.POST,instance=branch_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('branch:branchView',
                        kwargs={"action":"view","branchId":0}))
            else:
                return render(request,"branch/branch.html",
                  {"form":form,"branchID":branch_instance.id})
        else:
            return render(request,"branch/branch.html",
                  {"form":BranchForm(instance=branch_instance),"branchID":branch_instance.id,"action":"edit"})
    
    if action == "delete":
        branch_instance.delete()
        return HttpResponseRedirect(reverse('branch:branchView',
            kwargs={"action":"view","branchId":0}))
                 
    return render(request,"branch/branch.html",
                  {"form":BranchForm(),"branchID":0,"action":"add"})
    

# def branchProductView(request,branchProductId,action):
#     branch_products = Branch_Product.objects.all()
#     print(branch_products)
#     if branchProductId != 0:   
#         branch_product_instance = Branch_Product.objects.get(id=branchProductId)
    
#     if request.method == "POST" and action == "add":
#         form = BranchProductForm(data= request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('branch:branchProductView',
#             kwargs={"action":"view","branchProductId":0}))
#         else:
#             return render(request,"branch/branch_product.html",
#                   {"form":form,"branchProductId":0})  
            
    # if action == "edit":
    #     if request.method == "POST":
    #         form = BranchProductForm(data= request.POST,instance=branch_product_instance)
    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect(reverse('branch:branchProductView',
    #                     kwargs={"action":"view","branchProductId":0}))
    #         else:
    #             return render(request,"branch/branch_product.html",
    #               {"form":form,"branchProductId":branch_product_instance.id})
    #     else:
    #         return render(request,"branch/branch_product.html", 
    #               {"form":BranchProductForm(instance=branch_product_instance),
    #                "branchProducts":branch_products, "branchProductId":branch_product_instance.id,
    #                "action":"edit"})
    
    # if action == "delete":
    #     branch_product_instance.delete()
    #     return HttpResponseRedirect(reverse('branch:branchProductView',
    #         kwargs={"action":"view","branchProductId":0}))
                 
    # return render(request,"branch/branch_product.html",
    #               {"form":BranchProductForm(), "branchProducts":branch_products, "branchProductId":0,"action":"add"})
        
    