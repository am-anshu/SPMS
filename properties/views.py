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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Load the ML Model
with open('rent_predictor.pkl', 'rb') as file:
    model = pickle.load(file)

# Predict Rent Price Function
@login_required
def predict_rent(size, bedrooms, location_encoded):
    prediction = model.predict([[size, bedrooms, location_encoded]])
    return prediction[0]

# Add Property View

@login_required
def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST,request.FILES)
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

@login_required
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html',{"properties": properties, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY})


@login_required
def home(request):
    return render(request,'index.html')

# Tenant List
@login_required
def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenant_list.html', {'tenants': tenants})

@login_required
def maintenance_list(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance request added successfully!")
            return redirect('maintenance_list')  # Ensure 'maintenance_list' is the correct URL name
        else:
            messages.error(request, "Error adding maintenance request. Please check the form.")
    else:
        form = MaintenanceForm()

    maintenances = Maintenance.objects.all()
    return render(request, 'maintenance_list.html', {'form': form, 'maintenances': maintenances})







stripe.api_key = 'sk_test_51Qa8zlGay98PHNXshT4vIpR026lexDz3lTVXiCOBMBe4tSbWdDEyMS4gtEilZnlNFUPGlEWkk7wBNnNYWzsUQ7m000g2VfLjj7'
stripe.api_key = settings.STRIPE_SECRET_KEY



# Configure Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY





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
@login_required
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
            return  HttpResponse("<h2>Thank you for your message! We will get back to you soon.</h2></br>")
        except Exception as e:
            return HttpResponse(f"<h2>Error: {e}</h2>")
    return render(request, "contact_page.html")
@login_required
def about_page(request):
    return render(request,"about_page.html")



# Load the ML model
with open("rent_predictor.pkl", "rb") as file:
    rent_model = pickle.load(file)
@login_required
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


@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, "property_detail.html", {"property": property, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY})


# # Registration View
def new_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
       

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('new_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('new_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect('new_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('new_login')

    return render(request, 'new_register.html')


# Login View
def new_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home_page')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('new_login')

    return render(request, 'new_login.html')


# Logout View
def new_logout(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('new_login')



# from .forms import UserRegisterForm

# def register(request):
#     """ User registration view """
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Registration successful! You can now log in.")
#             return redirect("login")
#         else:
#             messages.error(request, "Error in registration. Please check your details.")
#     else:
#         form = UserRegisterForm()
#     return render(request, "new_register.html", {"form": form})

# def login_user(request):
#     """ User login view """
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome back, {user.username}!")
#             return redirect("property_list")
#         else:
#             messages.error(request, "Invalid username or password. Please try again.")
#     return render(request, "new_login.html")

# def logout_user(request):
#     """ User logout view """
#     logout(request)
#     messages.info(request, "You have been logged out.")
#     return redirect("login")