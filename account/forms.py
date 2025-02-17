from django import forms
from .models import Account
from django.core.exceptions import ValidationError

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'parent', 'status']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Account.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A account with this name already exists.")
        return name
