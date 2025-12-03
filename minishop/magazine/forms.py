from .models import *
from django import forms


class CreateForm(forms.Form):
    #product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'control mb-4'}))

    class Meta:
        model = Product
        fields = "__all__" #('product_name', 'regular_price', 'discounted_price', 'stock_quantity', 'product_details', 'category')
        widgets = {
            "product_name": forms.Textarea(attrs={'class': 'form-control mb-4'}),
        }

        """def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['product_name'].widget.attrs.update({'class': 'control mb-4'})

        field_classes = {
                    "product_name": forms.TextInput(attrs={'class': 'form-control mb-4'}),
                }"""