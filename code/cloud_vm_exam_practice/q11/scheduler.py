from collections import deque

# Task processing times in seconds (simulated).
tasks = [
    ("T1", 4), ("T2", 2), ("T3", 5),
    ("T4", 3), ("T5", 1), ("T6", 4)
]
workers = ["Worker-1", "Worker-2"]
queues = {w: deque() for w in workers}

for i, task in enumerate(tasks):
    queues[workers[i % len(workers)]].append(task)

completion = {}
for worker, queue in queues.items():
    elapsed = 0
    print(f"\n{worker}:")
    while queue:
        task, duration = queue.popleft()
        elapsed += duration
        completion[task] = elapsed
        print(f"  {task}: processing={duration}s, completion time={elapsed}s")

print("\nTasks assigned:")
for worker, queue in queues.items():
    pass
for worker in workers:
    assigned = [t for i, t in enumerate(tasks) if workers[i % len(workers)] == worker]
    print(f"  {worker}: {len(assigned)} tasks -> {[t[0] for t in assigned]}")
