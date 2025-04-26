class MyClass:
    def __init__(self, prop1=None, prop2=None):
        self.prop1 = prop1
        self.prop2 = prop2
        print("Объект создан")
    
    def __del__(self):
        print("Объект удален")

obj1 = MyClass()  # Создание с параметрами по умолчанию
obj2 = MyClass("значение1", "значение2")  # Создание с параметрами
del obj1  # Удаление объекта