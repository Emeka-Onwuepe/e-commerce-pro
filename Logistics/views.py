import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Logistics.form import LocationForm

from Logistics.models import Location
from Logistics.serializer import LocationSerializer


# Create your views here.

  
@login_required(login_url="logistics:loginView")   
def locationView(request,locationId,action):
    
    if request.method == "POST" and action == "get":
         data = json.loads(request.body.decode("utf-8"))
         locationdata = ""
         try:
            location = Location.objects.get(phone_number = data['phone_number'])
            locationdata = LocationSerializer(location).data
         except location.DoesNotExist:
             return JsonResponse({},status=404,reason="location not found.")
         return JsonResponse({"data":locationdata})
           
                     
    locations = Location.objects.all()
    if locationId != 0:   
        location_instance = Location.objects.get(id=locationId)
    
    if request.method == "POST" and action == "add":
        form = LocationForm(data= request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logistics:locationView',
            kwargs={"action":"view","locationId":0}))
        else:
            return render(request,"logistics/location.html",
                  {"form":form,"locationId":0,"action":"add"})  
            
    if action == "edit":
        if request.method == "POST":
            form = LocationForm(data= request.POST,instance=location_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('logistics:locationView',
                        kwargs={"action":"view","locationId":0}))
            else:
                return render(request,"logistics/location.html",
                  {"form":form,"locationId":location_instance.id,"action":"edit"})
        else:
            return render(request,"logistics/location.html",
                  {"form":LocationForm(instance=location_instance),
                   "locationId":location_instance.id,"action":"edit"})
    
    if action == "delete":
        location_instance.delete()
        return HttpResponseRedirect(reverse('logistics:locationView',
            kwargs={"action":"view","locationId":0}))
                 
    return render(request,"logistics/location.html",
                  {"form":LocationForm(),"locationId":0,"action":"add","locations":locations})    
