from django import forms
from .models import Property, Tenant, Maintenance

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))