def cart_item_count(request):
    cart = request.session.get("cart", {})
    total = sum(item["quantity"] for item in cart.values())
    return {"cart_count": total}
