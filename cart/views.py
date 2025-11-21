from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Product
from .cart import Cart

def cart_view(request):
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())
    
    return render(request, "cart/cart.html", {
        "cart": cart,
        "total": total,
    })

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect("cart")

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart")

def subtract_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.subtract(product)
    return redirect("cart")

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")

def checkout(request):
    cart = request.session.get("cart", {})
    total = sum(item["price"] * item["quantity"] for item in cart.values())

    if request.method == "POST":
        # Aquí luego guardamos la orden
        request.session["cart"] = {}
        return redirect("shop")

    return render(request, "cart/checkout.html", {
        "cart": cart,
        "total": total,
    })
