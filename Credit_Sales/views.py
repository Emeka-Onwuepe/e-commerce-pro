from urllib import request
from django.shortcuts import render
from Credit_Sales.forms import PaymentForm

from Credit_Sales.models import Credit_Sale, Payment

# Create your views here.

def creditSalesView(request):
    credits = []
    message =None
    if request.method == "POST":
        data = request.POST
        phone_number = data['phone_number']
        credits = Credit_Sale.objects.filter(
            customer__phone_number = phone_number, fully_paid=False )
        if not credits:
            message = "No data found. Please be sure the phone number is correct"
    return render(request,"credit_sales/credit.html",{"credits":credits,"message":message}) 

def paymentView(request,id,action):
    
    if action == "create":
        previous_payments = Payment.objects.filter(credit_sale=id)
        return render(request,"credit_sales/payments.html",
                      {"previous_payments":previous_payments,"form":PaymentForm()})
        