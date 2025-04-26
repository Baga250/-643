class Student:
    def __init__(self, surname, birth_date, group, grades):
        self.surname = surname
        self.birth_date = birth_date
        self.group = group
        self.grades = grades
    
    def change_surname(self, new_surname):
        self.surname = new_surname
    
    def change_birth_date(self, new_birth_date):
        self.birth_date = new_birth_date
    
    def change_group(self, new_group):
        self.group = new_group
    
    def display_info(self):
        print(f"Фамилия: {self.surname}")
        print(f"Дата рождения: {self.birth_date}")
        print(f"Группа: {self.group}")
        print(f"Успеваемость: {self.grades}")

student = Student("Иванов", "01.01.2000", "ГР-101", [4, 5, 3, 4, 5])
student.display_info()
student.change_surname("Петров")
student.change_group("ГР-102")
student.display_info()