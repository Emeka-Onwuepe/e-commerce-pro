from itertools import product
import json
import requests
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from Branch.models import Branch
from Logistics.models import Location
from Product.models import Category, Product, Product_Type, Size
from Sales.models import Items, Sales
from User.models import Customer
from SMBCLASSIC.variables import official_email,rootUrl,admin_staff

# Create your views here.
def homeView(request):
    products = Product.objects.all()[:10]    
    return render(request,'frontview/home.html',{"products":products})

def cartView(request): 
    locations = Location.objects.all()
    return render(request,'frontview/cart.html',{"public_key":settings.PAYSTACT_PUBLIC_KEY,
                                                 "locations":locations})

def categoryView(request,cat):
    category = get_object_or_404(Category,name__iexact=cat)
    unsorted_product_types = Product_Type.objects.filter(category=category.id,
                                                            product_type__publish = True)
    sorted_product_types = []
    for product_type in unsorted_product_types:
        if product_type not in sorted_product_types:
            sorted_product_types.append(product_type) 
    return render(request,'frontview/category.html',{"category":category,
                                                     "sorted_product_types":sorted_product_types})
    
    
def processPaymentView(request):
       if request.method == "POST":
           customer_instance = None
           sales = None
           sale_type = None
           data = json.loads(request.body.decode("utf-8"))
           
           if data['action'] == "payment":

               headers = {
                    "Authorization": f'Bearer {settings.PAYSTACT_SECRET_KEY}',
                        'Content-Type': 'application/json',
                }
               url = f'https://api.paystack.co/transaction/verify/{data["purchase_id"]}'
                
               response = requests.get(url,headers=headers)
                
               if response.status_code == 200:
                #    response_data = response.json()
                   sales = Sales.objects.get(purchase_id=data["purchase_id"])
                   sales.paid = True
                   sales.save()
                   email_body = (f"There is a new online sale with ID:{sales.purchase_id}. Please, view " +
                        f"sales details on {rootUrl}/sales/sale/{sales.purchase_id}/{sales.payment_method} ")
                   send_mail('A new order',email_body,official_email,[admin_staff])
                   return JsonResponse({"message":'success'})
                        
           if data['action'] == "create":
               
                orderlist = data['orders']
                
                try:
                    customer_instance = Customer.objects.get(phone_number = data['phone_number'])
                    customer_instance.phone_number = data["phone_number"]
                    customer_instance.email = data["email"]
                    customer_instance.name = data["name"]
                    customer_instance.address = data["address"]
                    customer_instance.save()
                except Customer.DoesNotExist:
                        customerData = {"phone_number":data["phone_number"], "email":data["email"],
                                "name":data["name"],"address":data["address"]}
                        customer_instance = Customer.objects.create(**customerData)
                
                branch = Branch.objects.get(branch__is_super_admin = True)
                sales = Sales.objects.create(branch=branch,
                                                    total_amount=data['total_amount'],
                                                    expected_amount=data['expected_amount'],
                                                    logistics=data['logistics'],
                                                    destination=data['address'],
                                                    remark = data['remark'],
                                                    channel ="web",
                                                    customer = customer_instance,
                                                    payment_method = data['payment_method'],
                                                    purchase_id = data['purchase_id'],
                                                    paid=False)
            
                for item in orderlist:
                        product = Product.objects.get(pk=int(item['id']))
                        size= None
                        if item['id'] != item['Id']:
                            _,sizeId= item['Id'].split("_")
                            size = Size.objects.get(pk=int(sizeId))
                        Item =  Items.objects.create(product=product,product_type=item['product_type'],
                                                size=item['size'],size_instance=size,color=item['color'],qty=item['qty'],
                                                unit_price=item['price'],total_price=item['productTotal'],
                                                mini_price=item['mini'],expected_price=item['expected'])
                        print(Item)
                        sales.items.add(Item)
                
                    
                return JsonResponse({"purchase_id":sales.purchase_id,
                                    "type":sale_type})


def customerOrderHistoryView(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        sales=[]
        if phone_number:
            sales = Sales.objects.filter(customer__phone_number = phone_number)
        return render(request,"frontview/orderhistory.html",{"orders":sales,"public_key":settings.PAYSTACT_PUBLIC_KEY})      
    return HttpResponseRedirect(reverse('frontview:cartView'))
        
def saleView(request,purchaseId):
    sale = get_object_or_404(Sales,purchase_id= purchaseId)
    return render(request,"frontview/saledetails.html",{"sale":sale,"customer":sale.customer})       