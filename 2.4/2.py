import sqlite3

class DrinkApp:
    def __init__(self, db_name='drinks.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        # Таблица для алкогольных напитков
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alcoholic_drinks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                strength REAL,
                quantity INTEGER
            )
        ''')
        
        # Таблица для ингредиентов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                quantity INTEGER
            )
        ''')
        
        # Таблица для коктейлей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                strength REAL,
                price REAL
            )
        ''')
        
        # Таблица состава коктейлей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cocktail_components (
                cocktail_id INTEGER,
                component_id INTEGER,
                component_type TEXT,  # 'alcohol' или 'ingredient'
                quantity INTEGER,
                FOREIGN KEY (cocktail_id) REFERENCES cocktails(id),
                PRIMARY KEY (cocktail_id, component_id, component_type)
            )
        ''')
        
        self.conn.commit()
    
    def add_alcoholic_drink(self, name, strength, quantity):
        self.cursor.execute('''
            INSERT INTO alcoholic_drinks (name, strength, quantity)
            VALUES (?, ?, ?)
        ''', (name, strength, quantity))
        self.conn.commit()
    
    def add_ingredient(self, name, quantity):
        self.cursor.execute('''
            INSERT INTO ingredients (name, quantity)
            VALUES (?, ?)
        ''', (name, quantity))
        self.conn.commit()
    
    def add_cocktail(self, name, components):
        # Сначала вычисляем крепость коктейля
        total_volume = 0
        total_alcohol = 0
        
        for component in components:
            if component['type'] == 'alcohol':
                self.cursor.execute('SELECT strength FROM alcoholic_drinks WHERE id = ?', (component['id'],))
                strength = self.cursor.fetchone()[0]
                total_alcohol += strength * component['quantity']
            total_volume += component['quantity']
        
        strength = (total_alcohol / total_volume) if total_volume > 0 else 0
        
        # Добавляем коктейль
        self.cursor.execute('''
            INSERT INTO cocktails (name, strength, price)
            VALUES (?, ?, ?)
        ''', (name, strength, 0))  # Цену можно вычислить аналогично
        
        cocktail_id = self.cursor.lastrowid
        
        # Добавляем компоненты
        for component in components:
            self.cursor.execute('''
                INSERT INTO cocktail_components (cocktail_id, component_id, component_type, quantity)
                VALUES (?, ?, ?, ?)
            ''', (cocktail_id, component['id'], component['type'], component['quantity']))
        
        self.conn.commit()
    
    def sell_cocktail(self, cocktail_id, quantity=1):
        # Проверяем наличие ингредиентов
        self.cursor.execute('''
            SELECT component_id, component_type, quantity 
            FROM cocktail_components 
            WHERE cocktail_id = ?
        ''', (cocktail_id,))
        components = self.cursor.fetchall()
        
        for component_id, component_type, needed_quantity in components:
            if component_type == 'alcohol':
                self.cursor.execute('SELECT quantity FROM alcoholic_drinks WHERE id = ?', (component_id,))
            else:
                self.cursor.execute('SELECT quantity FROM ingredients WHERE id = ?', (component_id,))
            
            available = self.cursor.fetchone()[0]
            if available < needed_quantity * quantity:
                raise ValueError(f"Недостаточно компонента {component_id}")
        
        # Уменьшаем количество ингредиентов
        for component_id, component_type, needed_quantity in components:
            if component_type == 'alcohol':
                self.cursor.execute('''
                    UPDATE alcoholic_drinks 
                    SET quantity = quantity - ? 
                    WHERE id = ?
                ''', (needed_quantity * quantity, component_id))
            else:
                self.cursor.execute('''
                    UPDATE ingredients 
                    SET quantity = quantity - ? 
                    WHERE id = ?
                ''', (needed_quantity * quantity, component_id))
        
        self.conn.commit()
    
    def restock(self, item_id, item_type, quantity):
        if item_type == 'alcohol':
            self.cursor.execute(''
                UPDATE alcoholic_drinks 
                SET quantity = quantity + ? 
                WHERE id = ?
            ''', (quantity, item_id))
        else:
            self.cursor.execute(''
                UPDATE ingredients 
                SET quantity = quantity + ? 
                WHERE id = ?
            ''', (quantity, item_id))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    app = DrinkApp()

    app.add_alcoholic_drink("Водка", 40, 100)
    app.add_alcoholic_drink("Ром", 35, 50)

    app.add_ingredient("Кола", 200)
    app.add_ingredient("Лимонный сок", 50)

    components = [
        {'id': 1, 'type': 'alcohol', 'quantity': 50},  # 50 мл водки
        {'id': 1, 'type': 'ingredient', 'quantity': 150}  # 150 мл колы
    ]
    app.add_cocktail("Водка-кола", components)
    
    app.sell_cocktail(1)
    
    app.restock(1, 'alcohol', 10)  # Добавляем 10 единиц водки
    
    app.close()