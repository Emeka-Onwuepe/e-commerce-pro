from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Product.form import CategoryForm, ProductForm, ProductTypeForm
from Product.models import Category, Product, Product_Type

# Create your views here.
def categoryView(request,categoryId,action):
    
    categories = Category.objects.all()
    
    if categoryId != 0:   
        category_instance = Category.objects.get(id=categoryId)
    
    if request.method == "POST" and action == "add":
        form = CategoryForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:categoryView',
            kwargs={"action":"view","categoryId":0}))
        else:
            return render(request,"product/category.html",
                  {"form":form,"categoryId":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = CategoryForm(data= request.POST,instance=category_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('product:categoryView',
                        kwargs={"action":"view","categoryId":0}))
            else:
                return render(request,"product/category.html",
                  {"form":form,"categoryId":category_instance.id})
        else:
            return render(request,"product/category.html",
                  {"form":CategoryForm(instance=category_instance),
                   "categoryId":category_instance.id,"action":"edit",'categories':categories})
    
    if action == "delete":
        category_instance.delete()
        return HttpResponseRedirect(reverse('product:categoryView',
            kwargs={"action":"view","categoryId":0}))
                 
    return render(request,"product/category.html",
                  {"form":CategoryForm(),"categoryId":0, 'categories':categories,"action":"add"})
    


def productTypeView(request,productTypeId,action):
    
    productTypes = Product_Type.objects.all()
    
    if productTypeId != 0:   
        product_type_instance = Product_Type.objects.get(id=productTypeId)
    
    if request.method == "POST" and action == "add":
        form = ProductTypeForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:productTypeView',
            kwargs={"action":"view","productTypeId":0}))
        else:
            return render(request,"product/product_type.html",
                  {"form":form,"productTypeId":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = ProductTypeForm(data= request.POST,instance=product_type_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('product:productTypeView',
                        kwargs={"action":"view","productTypeId":0}))
            else:
                return render(request,"product/product_type.html",
                  {"form":form,"productTypeId":product_type_instance.id})
        else:
            return render(request,"product/product_type.html",
                  {"form":ProductTypeForm(instance=product_type_instance),
                   "productTypeId":product_type_instance.id,"action":"edit",'productTypes':productTypes})
    
    if action == "delete":
        product_type_instance.delete()
        return HttpResponseRedirect(reverse('product:productTypeView',
            kwargs={"action":"view","productTypeId":0}))
                 
    return render(request,"product/product_type.html",
                  {"form":ProductTypeForm(),"productTypeId":0, 'productTypes':productTypes,"action":"add"})
    
    
def productView(request,productId,action):
    
    products = Product.objects.all()
    
    if productId != 0:   
        product_instance = Product.objects.get(id=productId)
    
    if request.method == "POST" and action == "add":
        form = ProductForm(data= request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:productView',
            kwargs={"action":"view","productId":0}))
        else:
            return render(request,"product/product.html",
                  {"form":form,"productId":0})  
            
    if action == "edit":
        if request.method == "POST":
            form = ProductForm(data= request.POST,files=request.FILES,instance=product_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('product:productView',
                        kwargs={"action":"view","productId":0}))
            else:
                return render(request,"product/product.html",
                  {"form":form,"productId":product_instance.id,"action":"edit",'products':products})
        else:
            return render(request,"product/product.html",
                  {"form":ProductForm(instance=product_instance),
                   "productId":product_instance.id,"action":"edit",'products':products})
    
    if action == "delete":
        product_instance.delete()
        return HttpResponseRedirect(reverse('product:productView',
            kwargs={"action":"view","productId":0}))
                 
    return render(request,"product/product.html",
                  {"form":ProductForm(),"productId":0, 'products':products,"action":"add"})