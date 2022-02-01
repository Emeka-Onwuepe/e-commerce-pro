from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Branch.models import Branch
from User.Forms import UserForm

# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
            user= request.user
            # return HttpResponseRedirect(reverse("publisher:publisherView",
            # kwargs={"username":user.full_name}))
    if request.method=="POST":
        form= AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user= authenticate(request, username=email, password=password)
            if user:
                login(request,user)
            return HttpResponseRedirect(reverse('user:dashboardView', kwargs={'fullname':user.full_name}))
    else:
        form=AuthenticationForm()
    return render(request,"user/login.html",{"form":form})

def logoutView(request):
    if request.method=="POST":
        logout(request)
    return HttpResponseRedirect(reverse('user:loginView'))

def dashboardView(request,fullname):
    branch_instance = Branch.objects.get(id=1)
    return render(request,"user/dashboard.html",{"userform": UserForm})