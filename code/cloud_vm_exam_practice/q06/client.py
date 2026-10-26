import Pyro4
uri = input("Enter server URI: ").strip()
service = Pyro4.Proxy(uri)
c = float(input("Temperature in Celsius: "))
print(f"{c:.2f} C = {service.celsius_to_fahrenheit(c):.2f} F")
service._pyroRelease()
