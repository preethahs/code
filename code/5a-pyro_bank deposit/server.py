
import Pyro4

@Pyro4.expose
class Bank:
    def __init__(self):
        self.balance = 1000

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return self.balance
        return "Insufficient balance"

daemon = Pyro4.Daemon()
uri = daemon.register(Bank())

print("Bank server ready. URI =", uri)
daemon.requestLoop()
