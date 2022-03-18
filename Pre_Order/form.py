from django import forms

from Pre_Order.models import Pre_Order

class PreOrderForm(forms.ModelForm):
    """Form definition for Pre_Order."""

    class Meta:
        """Meta definition for Pre_Orderform."""

        model = Pre_Order
        fields = ("product","customer","qty",'size_instance')
        
class PreOrder_Form(forms.ModelForm):
    """Form definition for Pre_Order."""

    class Meta:
        """Meta definition for Pre_Orderform."""

        model = Pre_Order
        fields = ("customer","qty")
        
