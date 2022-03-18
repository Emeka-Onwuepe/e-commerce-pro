from django import forms

from Stock.models import Stock


class StockForm(forms.ModelForm):
    """Form definition for Stock."""

    class Meta:
        """Meta definition for Stockform."""

        model = Stock
        fields =['qty','branch','product','size_instance']
        
class StockEditForm(forms.ModelForm):
    """Form definition for StockEdit."""
    
    class Meta:
        """Meta definition for StockEditform."""

        model = Stock
        fields = ['qty']