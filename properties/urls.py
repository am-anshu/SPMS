from django.urls import path
from . import views



urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('index/', views.home, name='home_page'),
    path('add/', views.add_property, name='add_property'),
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('maintainance/',views.maintenance_list,name='maintenance_list'),
    path("create-checkout-session/<int:property_id>/", views.create_checkout_session, name="create_checkout_session"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-cancel/", views.payment_cancel, name="payment_cancel"),
    path("contact-page/",views.contact_view,name="contact_page"),
    path("about-page/",views.about_page,name="about_page"),
    path("predict-rent/", views.predict_rent_view, name="predict_rent"),
    path("property/<int:property_id>/", views.property_detail, name="property_detail"),
    path('register/', views.new_register, name='new_register'),
    path('login/', views.new_login, name='new_login'),
    path('logout/', views.new_logout, name='new_logout'),
    
]
