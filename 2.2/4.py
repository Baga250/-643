class Counter:
    def __init__(self, value=0):
        self.value = value
    
    def increment(self):
        self.value += 1
    
    def decrement(self):
        self.value -= 1
    
    def get_value(self):
        return self.value

counter = Counter()
counter.increment()
counter.increment()
print(counter.get_value())  # 2
counter.decrement()
print(counter.get_value())  # 1

counter2 = Counter(10)
counter2.decrement()
print(counter2.get_value())  # 9