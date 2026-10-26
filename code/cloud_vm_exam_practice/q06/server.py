import Pyro4

@Pyro4.expose
class TemperatureConverter:
    def celsius_to_fahrenheit(self, celsius):
        return (float(celsius) * 9 / 5) + 32

daemon = Pyro4.Daemon()
uri = daemon.register(TemperatureConverter())
print("Temperature conversion RMI server running.")
print("URI:", uri)
daemon.requestLoop()
