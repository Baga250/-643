import psutil
import sqlite3
from datetime import datetime

class SystemMonitor:
    def __init__(self, db_name='system_monitor.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL
            )
        ''')
        self.conn.commit()
    
    def collect_stats(self):
        timestamp = datetime.now()
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        self.cursor.execute('''
            INSERT INTO system_stats 
            (timestamp, cpu_percent, memory_percent, disk_percent)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, cpu_percent, memory_percent, disk_percent))
        self.conn.commit()
        
        return {
            'timestamp': timestamp,
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent
        }
    
    def get_stats(self, start_time=None, end_time=None):
        query = 'SELECT * FROM system_stats'
        params = []
        
        if start_time and end_time:
            query += ' WHERE timestamp BETWEEN ? AND ?'
            params.extend([start_time, end_time])
        elif start_time:
            query += ' WHERE timestamp >= ?'
            params.append(start_time)
        elif end_time:
            query += ' WHERE timestamp <= ?'
            params.append(end_time)
        
        query += ' ORDER BY timestamp'
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    monitor = SystemMonitor()

    stats = monitor.collect_stats()
    print(f"CPU: {stats['cpu_percent']}%")
    print(f"Memory: {stats['memory_percent']}%")
    print(f"Disk: {stats['disk_percent']}%")

    history = monitor.get_stats()
    for record in history:
        print(record)
    
    monitor.close()