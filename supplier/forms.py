from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'address', 'phone', 'email', 'bank_name', 'account_name', 'account_number', 'bank_branch', 'status']
