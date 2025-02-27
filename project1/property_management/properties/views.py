from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from .models import Property, Tenant, Maintenance
from .forms import PropertyForm, TenantForm, MaintenanceForm
import pickle
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import ContactForm
from django.http import HttpResponse
# Load the ML Model
with open('rent_predictor.pkl', 'rb') as file:
    model = pickle.load(file)

# Predict Rent Price Function
def predict_rent(size, bedrooms, location_encoded):
    prediction = model.predict([[size, bedrooms, location_encoded]])
    return prediction[0]

# Add Property View

def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)

            # Use ML model for rent prediction
            location_encoded = 1  # Replace with actual location encoding logic
            predicted_rent = rent_model.predict(
                [[property_instance.size, property_instance.bedrooms, location_encoded]]
            )[0]
            property_instance.rent_price = predicted_rent
            property_instance.save()
            return redirect("property_list")
    else:
        form = PropertyForm()
    return render(request, "add_property.html", {"form": form})

# List Properties

def property_list(request):
    properties = Property.objects.all()
    return render(request, "property_list.html", {"properties": properties, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY})


# Tenant List
def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenant_list.html', {'tenants': tenants})

def maintenance_list(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    maintenances = Maintenance.objects.all()
    return render(request, 'maintenance_list.html', {'form': form, 'maintenances': maintenances})




# def buy_property(request, property_id):
#     property_instance = get_object_or_404(Property, id=property_id)
#     if property_instance.is_for_sale:
#         # Handle the property purchase logic here
#         property_instance.is_for_sale = False  # Mark as sold
#         property_instance.save()
#         return render(request, 'property_list.html', {'property': property_instance})
#     else:
#         return redirect('property_list')


stripe.api_key = 'sk_test_51Qa8zlGay98PHNXshT4vIpR026lexDz3lTVXiCOBMBe4tSbWdDEyMS4gtEilZnlNFUPGlEWkk7wBNnNYWzsUQ7m000g2VfLjj7'
stripe.api_key = settings.STRIPE_SECRET_KEY

# def payment_page(request, property_id):
#     property_instance = get_object_or_404(Property, id=property_id)
#     if request.method == 'POST':
#         # Stripe Payment Intent
#         try:
#             amount = int(property_instance.sale_price * 100)  # Convert dollars to cents
#             intent = stripe.PaymentIntent.create(
#                 amount=amount,
#                 currency='usd',
#                 payment_method=request.POST['payment_method_id'],
#                 confirmation_method='manual',
#                 confirm=True,
#             )
#             return render(request, 'payment_success.html', {'property': property_instance})
#         except stripe.error.CardError as e:
#             return render(request, 'payment_page.html', {
#                 'property': property_instance,
#                 'error': str(e.error.message),
#             })

#     return render(request, 'payment_page.html', {'property': property_instance})



# Configure Stripe with your secret key
# stripe.api_key = settings.STRIPE_SECRET_KEY



# Create a Stripe Checkout Session


# Configure Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create a Stripe Checkout Session
# def create_checkout_session(request, property_id):
#     try:
#         property = Property.objects.get(id=property_id)

#         # Create a Stripe Checkout Session
#         session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "product_data": {
#                             "name": property.name,
#                             "description": f"Location: {property.location}, Size: {property.size} sq ft",
#                         },
#                         "unit_amount": int(property.rent_price * 100),  # Amount in cents
#                     },
#                     "quantity": 1,
#                 }
#             ],
#             mode="payment",
#             success_url=f"http://localhost:8000/payment-success/?property_id={property.id}",
#             cancel_url="http://localhost:8000/payment-cancel/",
#         )
#         return JsonResponse({"id": session.id})
#     except Property.DoesNotExist:
#         return JsonResponse({"error": "Property not found"}, status=404)

# # Payment Success View
# def payment_success(request):
#     property_id = request.GET.get("property_id")
#     try:
#         property = Property.objects.get(id=property_id)
#         property.sold = True  # Assuming 'sold' field exists in Property model
#         property.save()
#         return render(request, "success.html", {"property": property})
#     except Property.DoesNotExist:
#         return render(request, "error.html", {"message": "Property not found"})

# # Payment Cancel View
# def payment_cancel(request):
#     return render(request, "cancel.html")






# Configure Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create a Stripe Checkout Session
def create_checkout_session(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if property.status == 'sold':
        return JsonResponse({"error": "Property already sold"}, status=400)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": property.name,
                            "description": f"Location: {property.location}, Size: {property.size} sq ft",
                        },
                        "unit_amount": int(property.rent_price * 100),  # Amount in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"http://localhost:8000/payment-success/?property_id={property.id}",
            cancel_url="http://localhost:8000/payment-cancel/",
        )
        return JsonResponse({"id": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Payment Success View
def payment_success(request):
    property_id = request.GET.get("property_id")
    property = get_object_or_404(Property, id=property_id)

    if property.status == 'sold':
        return render(request, "error.html", {"message": "Property already sold"})

    # Update property status to "Sold"
    property.status = 'sold'
    property.save()
    return render(request, "success.html", {"property": property})

# Payment Cancel View
def payment_cancel(request):
    return render(request, "cancel.html")

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        # Process the form data
        try:
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=message,
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],  # Replace with your email
            )
            return HttpResponse("<h2>Thank you for your message! We will get back to you soon.</h2>")
        except Exception as e:
            return HttpResponse(f"<h2>Error: {e}</h2>")
    return render(request, "contact_page.html")
def about_page(request):
    return render(request,"about_page.html")



# Load the ML model
with open("rent_predictor.pkl", "rb") as file:
    rent_model = pickle.load(file)

def predict_rent_view(request):
    if request.method == "POST":
        size = float(request.POST.get("size"))
        bedrooms = int(request.POST.get("bedrooms"))
        location_encoded = int(request.POST.get("location"))

        # Make prediction
        try:
            predicted_rent = rent_model.predict([[size, bedrooms, location_encoded]])
            return JsonResponse({"predicted_rent": predicted_rent[0]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return render(request, "predict_rent.html")



def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, "property_detail.html", {"property": property, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY})