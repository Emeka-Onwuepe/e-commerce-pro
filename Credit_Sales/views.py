from urllib import request
from coreapi import Object
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Credit_Sales.forms import PaymentForm

from Credit_Sales.models import Credit_Sale, Payment
from User.models import Customer

# Create your views here.
@login_required(login_url="user:loginView")
def creditSalesView(request,customerID,action):
    credits = []
    message =None
    settled = False
    customerid = customerID
    
    if request.method == "POST":
        data = request.POST
        phone_number = data['phone_number']
        
        credits = Credit_Sale.objects.filter(
            customer__phone_number = phone_number, fully_paid=False )
        if not credits:
            message = "No unsettled debts found"
        
        try:
            customer = Customer.objects.get(phone_number = phone_number)
            customerid = customer.id
        except Customer.DoesNotExist:
            message = "No customer found. Please be sure the phone number is correct"
        
        
    if action == "settled" and customerID>0:
        credits =  Credit_Sale.objects.filter(
            customer = customerID, fully_paid=True ) 
        settled = True
        if not credits: 
            message = "No settled debts found" 
    
    if customerID>0 and action != "settled":
        credits =  Credit_Sale.objects.filter(
            customer = customerID, fully_paid=False ) 
        try:
            customer = Customer.objects.get(pk = customerID)
            customerid = customer.id
        except Customer.DoesNotExist:
            pass
        
        if not credits: 
            message = "No unsettled debts found" 
        
    return render(request,"credit_sales/credit.html",{"credits":credits,
                                                      "message":message,
                                                      "settled":settled,
                                                      'customerid':customerid}) 

@login_required(login_url="user:loginView")
def paymentView(request,creditId,action):
    
    previous_payments = None
    customer = None
    paymentId= None
    payment_instance = None
    credit_sale = None
    try:
        credit_sale = Credit_Sale.objects.get(id= creditId)
    except Credit_Sale.DoesNotExist:
        pass
    
    if action =="add" or action =='view':
        customer = Customer.objects.get(credit_sale_customer__id = creditId)
        previous_payments = Payment.objects.filter(credit_sale=creditId)
        
    if action == "edit" or action =='delete':
        paymentId = creditId
        payment_instance = Payment.objects.get(pk=paymentId)
        creditId = payment_instance.credit_sale.id
        customer = Customer.objects.get(credit_sale_customer__id = creditId)
        previous_payments = Payment.objects.filter(credit_sale=creditId)

    if request.method == "POST" and action == "add":
        form = PaymentForm(data= request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            credit_sale = Credit_Sale.objects.get(pk=creditId)
            Payment.objects.create(amount=amount,credit_sale=credit_sale)
            return HttpResponseRedirect(reverse('credit_sales:paymentView',
            kwargs={"action":"view","creditId":creditId}))
        else:
            return render(request,"credit_sales/payment.html",
                  {"form":form,"creditId":creditId,
                   'customer':customer,"previous_payments":previous_payments})  
            
    if action == "edit":
        if request.method == "POST":
            form = PaymentForm(data= request.POST,instance=payment_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('credit_sales:paymentView',
                        kwargs={"action":"view","creditId":creditId}))
            else:
                return render(request,"credit_sales/payment.html",
                  {"form":form,"creditId":payment_instance.id,
                   'customer':customer,"previous_payments":previous_payments,
                   "credit_sale":credit_sale})
        else:
            return render(request,"credit_sales/payment.html",
                  {"form":PaymentForm(instance=payment_instance),
                   "creditId":payment_instance.id,"action":"edit",
                   'customer':customer,"previous_payments":previous_payments,
                   "credit_sale":credit_sale})
    
    if action == "delete":
        payment_instance.delete()
        return HttpResponseRedirect(reverse('credit_sales:paymentView',
            kwargs={"action":"view","creditId":creditId}))
    
    return render(request,"credit_sales/payment.html",
                      {"previous_payments":previous_payments,
                       "form":PaymentForm(),'creditId':creditId,"action":"add",
                       'customer':customer,"credit_sale":credit_sale})
        