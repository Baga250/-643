class Train:
    def __init__(self, destination, number, departure_time):
        self.destination = destination
        self.number = number
        self.departure_time = departure_time
    
    def display_info(self):
        print(f"Пункт назначения: {self.destination}")
        print(f"Номер поезда: {self.number}")
        print(f"Время отправления: {self.departure_time}")

train = Train("Москва", "123А", "12:30")
train.display_info()