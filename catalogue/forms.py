from django.forms import  ModelForm, ModelChoiceField
from .models import  Order, Product

class CreateOrderForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects, empty_label="Select a product")
    class Meta:
        model = Order
        fields = ['product', 'amount']