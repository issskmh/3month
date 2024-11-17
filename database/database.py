import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL, 
                name TEXT NOT NULL,
                contact_info TEXT NOT NULL,
                visit_date DATE NOT NULL,
                food_rating INTEGER NOT NULL,
                cleanliness_rating INTEGER NOT NULL,
                extra_comments TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def execute(self, query: str, params: tuple = ()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
