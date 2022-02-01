from django import forms
from Branch.models import Branch, Branch_Product

class BranchForm(forms.ModelForm):
    # name = forms.CharField()
    # branch_products = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple ,
    #                                                  queryset=Branch_Product.objects.all())
    class Meta:
        model = Branch
        fields = '__all__'
        
class BranchProductForm(forms.ModelForm):
    """Form definition for BranchProduct."""

    class Meta:
        """Meta definition for BranchProductform."""

        model = Branch_Product
        fields = '__all__'
