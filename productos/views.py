from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .models import Product, Category

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Filtro por búsqueda
    search = request.GET.get("search")
    if search:
        products = products.filter(name__icontains=search)

    # Filtro por categoría
    cat_id = request.GET.get("category")
    if cat_id:
        products = products.filter(category_id=cat_id)

    return render(request, "shop.html", {
        "categories": categories,
        "products": products,
    })
    
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect("cart")
    
    
#def add_to_cart(request, product_id):
#    product = get_object_or_404(Product, id=product_id)
#
#    cart = request.session.get("cart", {})
#
#    # si el producto ya existe, sumar +1
#    if str(product_id) in cart:#
#        cart[str(product_id)]["quantity"] += 1
#    else:
#        cart[str(product_id)] = {
#            "name": product.name,
#            "price": float(product.price),
#            "image": product.image.url,
#            "quantity": 1,
#        }
#
#    request.session["cart"] = cart
#    return redirect("shop")

################