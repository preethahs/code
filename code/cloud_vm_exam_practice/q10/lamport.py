class LamportClock:
    def __init__(self, process_id):
        self.process_id = process_id
        self.time = 0

    def local_event(self):
        self.time += 1
        print(f"P{self.process_id}: local event -> {self.time}")

    def send_event(self):
        self.time += 1
        print(f"P{self.process_id}: send message timestamp={self.time}")
        return self.time

    def receive_event(self, received_time):
        self.time = max(self.time, received_time) + 1
        print(f"P{self.process_id}: receive message -> {self.time}")

p1 = LamportClock(1)
p2 = LamportClock(2)
p1.local_event()
timestamp = p1.send_event()
p2.receive_event(timestamp)
p2.local_event()
