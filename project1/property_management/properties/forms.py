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
