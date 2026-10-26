import Pyro4
uri = input("Enter server URI: ").strip()
shop = Pyro4.Proxy(uri)
print("Available products and prices:")
for product, price in shop.list_products().items():
    print(f"  {product}: Rs. {price:.2f}")
product = input("Product name: ")
quantity = int(input("Quantity: "))
result = shop.checkout(product, quantity)
if "error" in result:
    print("Error:", result["error"])
else:
    print("Subtotal: Rs.", result["subtotal"])
    print(f"Discount ({result['discount_percent']}%): Rs. {result['discount']:.2f}")
    print(f"Final amount: Rs. {result['final_amount']:.2f}")
shop._pyroRelease()
