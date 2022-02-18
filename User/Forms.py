from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("full_name","email","phone_number","branch",)
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name","email","phone_number","branch",)
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name","email","phone_number","address",)