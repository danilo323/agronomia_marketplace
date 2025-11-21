class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if "cart" not in self.session:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "name": product.name,
                "price": float(product.price),
                "image": product.image.url,
                "quantity": 1,
            }
        else:
            self.cart[product_id]["quantity"] += 1

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def subtract(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= 1

            if self.cart[product_id]["quantity"] <= 0:
                del self.cart[product_id]

            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
