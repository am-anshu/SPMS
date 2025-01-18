from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('add/', views.add_property, name='add_property'),
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('maintainance/',views.maintenance_list,name='maintenance_list'),
    # path('buy/<int:property_id>/', views.buy_property, name='buy_property'),
    # path('buy/<int:property_id>/', views.payment_page, name='payment_page'),
    path("create-checkout-session/<int:property_id>/", views.create_checkout_session, name="create_checkout_session"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-cancel/", views.payment_cancel, name="payment_cancel"),
    # path('buy/<int:property_id>/', views.buy_property, name='buy_property'),
    # path('payment-success/<int:property_id>/', views.payment_success, name='payment_success'),
    path("", views.property_list, name="property_list"),
    # path("create-checkout-session/<int:property_id>/", views.create_checkout_session, name="create_checkout_session"),
    # path("payment-success/", views.payment_success, name="payment_success"),
    # path("payment-cancel/", views.payment_cancel, name="payment_cancel"),
    path("contact-page/",views.contact_view,name="contact_page"),
    path("about-page/",views.about_page,name="about_page"),
    path("predict-rent/", views.predict_rent_view, name="predict_rent"),
    path("property/<int:property_id>/", views.property_detail, name="property_detail"),
]
