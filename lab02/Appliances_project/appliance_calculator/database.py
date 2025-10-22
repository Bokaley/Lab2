import sqlite3
import datetime
from typing import List, Dict, Union, Optional

# Сохранение результатов в БД (sqlite3)
class DatabaseManager:
    """
    Класс для управления базой данных SQLite.
    """
    def __init__(self, db_name: str = "energy_consumption.db"):
        if not isinstance(db_name, str) or not db_name.endswith(".db"):
            raise ValueError("Имя базы данных должно быть строкой, оканчивающейся на .db")
        self.db_name = db_name
        self._conn = None
        self._cursor = None
        self._connect()
        self._create_table()

    def _connect(self):
        """Устанавливает соединение с БД."""
        try:
            self._conn = sqlite3.connect(self.db_name)
            self._cursor = self._conn.cursor()
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def _create_table(self):
        """Создает таблицу для хранения данных, если она не существует."""
        try:
            self._cursor.execute("""
                CREATE TABLE IF NOT EXISTS consumption_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    appliance_name TEXT NOT NULL,
                    power_consumption_watts INTEGER NOT NULL,
                    hours_used REAL NOT NULL,
                    consumption_kwh REAL NOT NULL,
                    cost REAL NOT NULL,
                    tariff REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            self._conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")
            raise

    def save_record(self, appliance_name: str, power_consumption_watts: int, hours_used: float, consumption_kwh: float, cost: float, tariff: float):
        """Сохраняет одну запись о потреблении."""
        timestamp = datetime.datetime.now().isoformat()
        try:
            self._cursor.execute("""
                INSERT INTO consumption_records (appliance_name, power_consumption_watts, hours_used, consumption_kwh, cost, tariff, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (appliance_name, power_consumption_watts, hours_used, consumption_kwh, cost, tariff, timestamp))
            self._conn.commit()
            print(f"Запись сохранена в БД: {appliance_name}")
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении записи: {e}")
            raise

    def get_all_records(self) -> List[Dict[str, Union[str, int, float]]]:
        """Возвращает все записи из БД."""
        try:
            self._cursor.execute("SELECT * FROM consumption_records ORDER BY timestamp DESC")
            rows = self._cursor.fetchall()
            column_names = [description[0] for description in self._cursor.description]

            results = []
            for row in rows:
                record_dict = {}
                for i, col_name in enumerate(column_names):
                    record_dict[col_name] = row[i]
                results.append(record_dict)
            return results
        except sqlite3.Error as e:
            print(f"Ошибка при получении записей: {e}")
            return []

    # 2 dunder-метода
    def __str__(self) -> str:
        return f"Менеджер БД SQLite (файл: {self.db_name})"

    def __repr__(self) -> str:
        return f"DatabaseManager(db_name='{self.db_name}')"

    def close(self):
        """Закрывает соединение с БД."""
        if self._conn:
            self._conn.close()
            print("Соединение с БД закрыто.")
