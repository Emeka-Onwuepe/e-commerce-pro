from unicodedata import category
from django.shortcuts import render

from Product.models import Category, Product_Type

# Create your views here.

def homeView(request):
    return render(request,'frontview/home.html')

def categoryView(request,catId):
    category = Category.objects.get(pk=catId)
    unsorted_product_types = Product_Type.objects.filter(category=category.id,
                                                            product_type__publish = True)
    sorted_product_types = []
    for product_type in unsorted_product_types:
        if product_type not in sorted_product_types:
            sorted_product_types.append(product_type) 
    return render(request,'frontview/category.html',{"category":category,
                                                     "sorted_product_types":sorted_product_types})