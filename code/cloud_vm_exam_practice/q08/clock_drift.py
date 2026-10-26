# Clock B gains 10 milliseconds each second compared with clock A.
duration_seconds = 60
drift_ms_per_second = 10
difference_ms = duration_seconds * drift_ms_per_second
print("Duration:", duration_seconds, "seconds")
print("Clock A elapsed time:", duration_seconds, "seconds")
print("Clock B elapsed time:", duration_seconds + difference_ms / 1000, "seconds")
print(f"Difference after 1 minute: {difference_ms} ms ({difference_ms/1000:.3f} seconds)")
