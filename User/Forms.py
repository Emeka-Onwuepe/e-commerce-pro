from django import forms
from .models import Customer, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name","email","phone_number","branch",)
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("full_name","email","phone_number","address",)