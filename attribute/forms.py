from django import forms
from .models import Attribute, AttributeValue
from django.core.exceptions import ValidationError

class AttributeForm(forms.ModelForm):
    # The `values` field remains optional for the dynamic input handling
    values = forms.CharField(
        help_text="Add values separated by commas or dynamically using the interface", 
        required=False
    )
    
    # Option field
    option = forms.ChoiceField(
        choices=Attribute.OPTION_CHOICES, 
        required=True, 
        help_text="Select the option type for this attribute"
    )

    class Meta:
        model = Attribute
        fields = ['name', 'option', 'values']  # Include 'option' and 'values'

    def clean(self):
        cleaned_data = super().clean()
        # Fetch dynamically added values from POST
        dynamic_values = self.data.getlist('values[]')  # Handles dynamic inputs from the front end

        # Ensure at least one valid value is provided
        if not dynamic_values or all(not value.strip() for value in dynamic_values):
            raise ValidationError("Please provide at least one value.")
        
        # Store cleaned dynamic values back into cleaned_data
        cleaned_data['values'] = ', '.join(value.strip() for value in dynamic_values if value.strip())
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

            # Clear existing AttributeValue instances for this attribute
            AttributeValue.objects.filter(attribute=instance).delete()

            # Split and save new values as individual AttributeValue instances
            values = self.cleaned_data['values'].split(',')
            for value in values:
                value = value.strip()
                if value:  # Avoid empty values
                    AttributeValue.objects.create(attribute=instance, value=value)

        return instance
