class Lamportclock:
    def __init__(self,pid):
        self.pid=pid
        self.clock=0

    def internal_event(self):
        self.clock+=1
        print("Process:",self.pid,"Event:",self.clock)

    def send_event(self):
        self.clock+=1
        print("Process:",self.pid, "Send:",self.clock)
        return self.clock
    
    def receive_event(self,t):
        self.clock=max(self.clock,t)+1
        print("Process:",self.pid,"Receive:",self.clock)

p1=Lamportclock(1)
p2=Lamportclock(2)

p1.internal_event()
t=p1.send_event()
p2.receive_event(t)
p2.internal_event()



    