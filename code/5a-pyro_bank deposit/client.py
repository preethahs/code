
import Pyro4

uri = input("Enter the bank object URI: ").strip()
bank = Pyro4.Proxy(uri)

print("1. Deposit")
print("2. Withdraw")

choice = input("Enter choice: ")
amount = int(input("Enter amount: "))

if choice == "1":
    print("Balance:", bank.deposit(amount))
elif choice == "2":
    print("Balance:", bank.withdraw(amount))
else:
    print("Invalid choice")
