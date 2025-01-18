from django.db import models

# Create your models here.
from django.db import models

# Property Model
# class Property(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     size = models.FloatField()  # in sq. ft
#     bedrooms = models.IntegerField()
#     rent_price = models.FloatField(blank=True, null=True)  # predicted price
#     image = models.ImageField(upload_to='property_images/', blank=True, null=True)
#     is_for_sale = models.BooleanField(default=False)
#     sale_price = models.FloatField(blank=True, null=True)
#     def __str__(self):
#         return self.name
class Property(models.Model):
    STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('sold', 'Sold'),
    ]
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    size = models.FloatField()  # in sq. ft
    bedrooms = models.IntegerField()
    rent_price = models.FloatField(blank=True, null=True)  # price in USD
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
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
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    issue = models.CharField(max_length=200)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Maintenance for {self.property.name}"
        # return self.property.name
