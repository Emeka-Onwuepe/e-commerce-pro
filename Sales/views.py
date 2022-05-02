from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from Branch.models import Branch
from Credit_Sales.models import Credit_Sale
from Product.models import Product, Product_Type, Size
from Sales.form import salesForm
from Sales.models import Items, Sales
from User.Forms import CustomerForm
from User.models import Customer

# Create your views here.
@login_required(login_url="user:loginView")
def salesView(request):
    if request.method == "POST":
        products=[]
        found = False
        data = request.POST['data']
        product_type = Product_Type.objects.filter(name__icontains =data)
        for item in product_type:   
            product = Product.objects.filter(branches=request.user.branch,
                                             product_type = item.id)
            if product:
                found = True
            products.append(product)
            print(products)
        return render(request,"sales/sales.html",
                          {'products':products, 'initial':False,"found":found,
                           "customerForm":CustomerForm, "saleForm":salesForm})
    return render(request,"sales/sales.html",{'initial':True,'found':False,
                                              "customerForm":CustomerForm, "saleForm":salesForm})

@login_required(login_url="user:loginView")
def saleView(request,purchaseId,type):
    sale = None
    customer = None
    not_found = False
    try:
        if type == 'credit':
            sale = Credit_Sale.objects.get(purchase_id= purchaseId)
            customer = sale.customer
        else:
            sale = Sales.objects.get(purchase_id= purchaseId)
            customer = sale.customer
    except (Credit_Sale.DoesNotExist,Sales.DoesNotExist):
        not_found = True
  
    
    
    return render(request,"sales/sale.html",{"sale":sale,
                                             "customer":customer,'not_found':not_found})

@login_required(login_url="user:loginView")
def salesProductView(request,productTypeId):
    products = []
    initial = True
    if productTypeId != 0:
        initial = False
        products = Product.objects.filter(product_type = productTypeId,
                                      branches=request.user.branch)
    return render(request,"sales/product.html",{"products":products,"customerForm":CustomerForm,
                                                "saleForm":salesForm,'initial':initial})

@login_required(login_url="user:loginView")
def processSalesView(request):
   if request.method == "POST":
       customer_instance = None
       credit_or_sales = None
       sale_type = None
       data = json.loads(request.body.decode("utf-8"))
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
       
       if data['payment_method'] == "credit":
           credit_or_sales = Credit_Sale.objects.create(branch=request.user.branch,
                                               total_amount=float(data['total_amount']),
                                               expected_amount=float(data['expected_amount']),
                                               remark = data['remark'],
                                               customer = customer_instance,
                                               purchase_id = data['purchase_id'])
       else:
           credit_or_sales = Sales.objects.create(branch=request.user.branch,
                                               total_amount=data['total_amount'],
                                               expected_amount=data['expected_amount'],
                                               remark = data['remark'],
                                               channel ="store",
                                               customer = customer_instance,
                                               payment_method = data['payment_method'],
                                               purchase_id = data['purchase_id'])
           sale_type = credit_or_sales.payment_method
       
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
            credit_or_sales.items.add(Item)
         
           
       return JsonResponse({"purchase_id":credit_or_sales.purchase_id,
                            "type":sale_type})
       
@login_required(login_url="user:loginView")     
def salesAnalysisView(request,date,branchID):
    
    selected_branch = request.user.branch
    
    if branchID != 0 and request.user.is_admin:
        selected_branch = branchID
    
    if date == "default":
        date = datetime.today().strftime('%Y-%m-%d')
         
    store = Items.objects.filter(items__date=date,items__channel='store',items__branch=selected_branch)
    transfer_total = Items.objects.filter(items__date=date,
                                       items__payment_method='transfer',
                                       items__branch=selected_branch).aggregate(total=Sum("total_price"))
    cash_total = Items.objects.filter(items__date=date,
                                items__branch=selected_branch,
                                       items__payment_method='cash').aggregate(total=Sum("total_price"))
    credit =  Items.objects.filter(credit_sale_Items__date =date,credit_sale_Items__branch=selected_branch)
    online = Items.objects.filter(items__date=date,items__channel='web',items__paid=True)
    
    day_data ={
        "store_sales":{
            # "transferData":transfer,
            # "cashData":cash,
            "sales": store,
            "summary":store.values("product_type").annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "transfer":transfer_total,
            "cash": cash_total,
            "total_amount":store.aggregate(total=Sum("total_price"))
        },
        "credit_sales":{
            "sales": credit,
            "summary": credit.values("product_type").annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":credit.aggregate(total=Sum("total_price")),
        }
    }
    
    if request.user.is_admin:
        online = {
            "sales": online,
            "summary": online.values("product_type").annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":online.aggregate(total=Sum("total_price"),logistics=Sum('items__logistics')),
        }
        
        branches = Branch.objects.all()
    
        day_data["online_sales"] = online
        day_data["branches"] = branches
           
    return render(request,"sales/daysales.html",day_data)

@login_required(login_url="user:loginView")
def rangeSalesView(request,start_date,end_date,branchID):

    selected_branch = request.user.branch.id
    
    if branchID != 0 and request.user.is_admin:
        selected_branch = branchID
    
    branch_instance = Branch.objects.get(pk=selected_branch)
    
    store = Items.objects.filter(items__date__range=[start_date,end_date],
                                 items__channel='store',items__branch=selected_branch)
    credit =  Items.objects.filter(credit_sale_Items__date__range=[start_date,end_date],
                                   credit_sale_Items__branch=selected_branch)
    online = Items.objects.filter(items__date__range=[start_date,end_date],
                                  items__branch=selected_branch, items__channel='web', items__paid=True)
    
    data ={
        "store_sales":{
            "summary":store.values('items__date',"product_type").annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":store.aggregate(total=Sum("total_price"))
        },
        "credit_sales":{
            "summary": credit.values('credit_sale_Items__date',"product_type").annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":credit.aggregate(total=Sum("total_price")),
        }
    }
    
    if request.user.is_admin:
        online = {
            "summary": online.values('items__date',"product_type").annotate(
                        total_amount=Sum("total_price"),total_qty =Sum("qty")),
            "total_amount":online.aggregate(total=Sum("total_price"),logistics=Sum("items__logistics")),
        }
    
        data["online_sales"] = online
    
    data["branch"] = branch_instance
    data['title'] = f'Range Sales: {start_date} -- {end_date}  '     
    return render(request,"sales/rangesales.html",data)      
