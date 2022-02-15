from django import forms
from Sales.models import Sales


class salesForm(forms.ModelForm):
    """Form definition for sales."""

    class Meta:
        """Meta definition for salesform."""

        model = Sales
        fields = ('customer_name','phone_number',
                  'email','address','payment_method','remark')
        widgets = {
            "remark" : forms.widgets.Textarea()     
            }
