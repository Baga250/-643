class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days
    
    def get_salary(self):
        return self.rate * self.days

worker = Worker("Иван", "Иванов", 1000, 20)
print(f"Зарплата: {worker.get_salary()}")