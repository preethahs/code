import Pyro4

@Pyro4.expose
class ShoppingService:
    def __init__(self):
        self.products = {
            "laptop": 60000.0,
            "mouse": 800.0,
            "keyboard": 1500.0,
            "headphones": 2500.0
        }

    def list_products(self):
        return self.products

    def checkout(self, product, quantity):
        product = product.lower().strip()
        quantity = int(quantity)
        if product not in self.products:
            return {"error": "Product not found", "products": self.products}
        if quantity <= 0:
            return {"error": "Quantity must be positive"}
        subtotal = self.products[product] * quantity
        discount_rate = 0.10 if subtotal >= 5000 else 0.0
        discount = subtotal * discount_rate
        return {"product": product, "unit_price": self.products[product],
                "quantity": quantity, "subtotal": round(subtotal, 2),
                "discount_percent": int(discount_rate * 100),
                "discount": round(discount, 2),
                "final_amount": round(subtotal - discount, 2)}

daemon = Pyro4.Daemon()
uri = daemon.register(ShoppingService())
print("Online shopping RMI server running.")
print("URI:", uri)
daemon.requestLoop()
