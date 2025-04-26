class TwoNumbers:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    
    def display_numbers(self):
        print(f"Число 1: {self.num1}")
        print(f"Число 2: {self.num2}")
    
    def change_numbers(self, new_num1, new_num2):
        self.num1 = new_num1
        self.num2 = new_num2
    
    def sum_numbers(self):
        return self.num1 + self.num2
    
    def max_number(self):
        return max(self.num1, self.num2)

numbers = TwoNumbers(5, 10)
numbers.display_numbers()
print(f"Сумма: {numbers.sum_numbers()}")
print(f"Максимальное: {numbers.max_number()}")
numbers.change_numbers(7, 3)
numbers.display_numbers()