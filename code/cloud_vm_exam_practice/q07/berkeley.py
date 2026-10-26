# Simplified Berkeley clock synchronization simulation.
clocks = {"Coordinator": 10.0, "Node-A": 8.5, "Node-B": 11.2, "Node-C": 9.3}
coordinator = clocks["Coordinator"]
offsets = {name: value - coordinator for name, value in clocks.items() if name != "Coordinator"}
average_offset = sum(offsets.values()) / (len(offsets) + 1)  # coordinator offset is 0
print("Initial clock values (seconds):")
for name, value in clocks.items():
    print(f"  {name}: {value:.2f}")
print("\nOffsets from coordinator:")
for name, offset in offsets.items():
    print(f"  {name}: {offset:+.2f} s")
print(f"\nAverage offset including coordinator: {average_offset:+.3f} s")
print("\nAdjustments to apply:")
for name, value in clocks.items():
    offset = value - coordinator
    adjustment = average_offset - offset
    print(f"  {name}: {adjustment:+.3f} s")
print("\nAfter synchronization (idealized):")
for name, value in clocks.items():
    offset = value - coordinator
    print(f"  {name}: {value + (average_offset - offset):.3f} s")
