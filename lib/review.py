import sqlite3  # Example for SQLite, adjust as per your actual database

# Establish database connection
CONNECTION = sqlite3.connect('your_database.db')
CURSOR = CONNECTION.cursor()

class Review:
    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                year INTEGER NOT NULL,
                summary TEXT NOT NULL,
                employee_id INTEGER NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        """)
        CONNECTION.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS reviews")
        CONNECTION.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """, (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid
        else:
            self.update()
        CONNECTION.commit()

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        if row:
            return cls(row[1], row[2], row[3], id=row[0])
        return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM reviews WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row)

    def update(self):
        CURSOR.execute("""
            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """, (self.year, self.summary, self.employee_id, self.id))
        CONNECTION.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM reviews WHERE id = ?", (self.id,))
        CONNECTION.commit()

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM reviews")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
