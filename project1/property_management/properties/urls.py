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
]
