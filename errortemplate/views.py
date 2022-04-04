from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def page_not_found(request,exception):
    temp_page = 'errortemplate/404.html'
    if request.user.is_authenticated:
        temp_page = 'errortemplate/staff_404.html'   
    return render(request,temp_page)

def permission_denied(request, exception):
    temp_page = 'errortemplate/403.html'
    if request.user.is_authenticated:
        temp_page = 'errortemplate/staff_403.html'   
    return render(request,temp_page)

def bad_request(request, exception):
    temp_page = 'errortemplate/400.html'
    if request.user.is_authenticated:
        temp_page = 'errortemplate/staff_400.html'   
    return render(request,temp_page)