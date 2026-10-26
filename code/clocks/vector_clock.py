class VectorClock:
    def __init__(self,pid,n):
        self.pid=pid
        self.n=n
        self.vector=[0]*n

    def internal_event(self):
        self.vector[self.pid]+=1
        print("Process:",self.pid,"Event:",self.vector)

    def send_event(self):
        self.vector[self.pid]+=1
        print("Process:",self.pid,"Send:",self.vector)
        return self.vector.copy()

    def receive_event(self,t):
        for i in range(self.n):
            self.vector[i]=max(self.vector[i],t[i])
        self.vector[self.pid]+=1
        print("Process:",self.pid,"Receive:",self.vector)

p1=VectorClock(0,3)
p2=VectorClock(1,3)
p3=VectorClock(2,3)

p1.internal_event()
t=p1.send_event()
p2.receive_event(t)
p2.internal_event()
t=p2.send_event()
p3.receive_event(t)
p3.internal_event()

