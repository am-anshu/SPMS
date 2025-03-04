from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
# from properties.models import Property  # Assuming you have a Property model



class Property(models.Model):
    STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('sold', 'Sold'),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    location = models.CharField(max_length=100)
    size = models.FloatField()  # in sq. ft
    bedrooms = models.IntegerField()
    rent_price = models.FloatField(blank=True, null=True)  # price in USD
    sale_price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # New field for details
    

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='for_sale',
    )  # Default status is "For Sale"

    def __str__(self):
        return self.name

# Tenant Model
class Tenant(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    move_in_date = models.DateField()
    
    def __str__(self):
        return self.name

# Maintenance Model

class Maintenance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="maintenance_requests")
    issue = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_resolved(self):
        return self.status == "resolved"

    def __str__(self):
        return f"{self.property.name} - {self.issue} ({self.get_status_display()})"
