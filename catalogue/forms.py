from django.forms import  ModelForm
from .models import  Order

class CreateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'amount']