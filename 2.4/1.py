import sqlite3
from dataclasses import dataclass

@dataclass
class Student:
    first_name: str
    last_name: str
    middle_name: str
    group: str
    grades: list

class StudentApp:
    def __init__(self, db_name='students.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT,
                group_name TEXT,
                grade1 INTEGER,
                grade2 INTEGER,
                grade3 INTEGER,
                grade4 INTEGER
            )
        ''')
        self.conn.commit()
    
    def add_student(self, student):
        self.cursor.execute('''
            INSERT INTO students 
            (first_name, last_name, middle_name, group_name, grade1, grade2, grade3, grade4)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student.first_name,
            student.last_name,
            student.middle_name,
            student.group,
            *student.grades
        ))
        self.conn.commit()
    
    def get_all_students(self):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()
    
    def get_student(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        return self.cursor.fetchone()
    
    def update_student(self, student_id, student):
        self.cursor.execute('''
            UPDATE students SET
            first_name = ?,
            last_name = ?,
            middle_name = ?,
            group_name = ?,
            grade1 = ?,
            grade2 = ?,
            grade3 = ?,
            grade4 = ?
            WHERE id = ?
        ''', (
            student.first_name,
            student.last_name,
            student.middle_name,
            student.group,
            *student.grades,
            student_id
        ))
        self.conn.commit()
    
    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        self.conn.commit()
    
    def get_group_average(self, group_name):
        self.cursor.execute('''
            SELECT AVG((grade1 + grade2 + grade3 + grade4) / 4.0)
            FROM students
            WHERE group_name = ?
        ''', (group_name,))
        return self.cursor.fetchone()[0]
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    app = StudentApp()
    
    student = Student("Иван", "Иванов", "Иванович", "ГР-101", [5, 4, 5, 4])
    app.add_student(student)
    
    print(app.get_all_students())
    
    print(f"Средний балл группы ГР-101: {app.get_group_average('ГР-101')}")
    
    app.close()