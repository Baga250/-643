class Calculation:
    def __init__(self):
        self.calculationLine = ""
    
    def set_calculation_line(self, new_value):
        self.calculationLine = new_value
    
    def set_last_symbol_calculation_line(self, symbol):
        self.calculationLine += symbol
    
    def get_calculation_line(self):
        return self.calculationLine
    
    def get_last_symbol(self):
        return self.calculationLine[-1] if self.calculationLine else None
    
    def delete_last_symbol(self):
        if self.calculationLine:
            self.calculationLine = self.calculationLine[:-1]

calc = Calculation()
calc.set_calculation_line("123")
calc.set_last_symbol_calculation_line("+")
print(calc.get_calculation_line())
print(calc.get_last_symbol())
calc.delete_last_symbol()
print(calc.get_calculation_line())