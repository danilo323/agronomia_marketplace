from django.urls import path
from . import views

urlpatterns = [
    path("shop/", views.shop, name="shop"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
]