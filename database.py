import sqlite3
import datetime, time

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("tasktracker.db")
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.connection.cursor()

    # Connection
    def create_database(self):
        with open("schema.sql", "r") as file:
            self.cursor.executescript(file.read())

        self.connection.commit()

    def close(self):
        self.connection.close()

    # Categories
    def add_category(self, category):
        sql = """
              INSERT INTO Categories (category_name, category_colour, category_icon)
              VALUES (?, ?, ?) \
              """

        self.cursor.execute(sql, (
            category.category_name,
            category.category_colour,
            category.category_icon
        ))

        self.connection.commit()

    def get_categories(self):
        sql = "SELECT * FROM Categories"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_category(self, category_id):
        sql = "SELECT * FROM Categories WHERE category_id = ?"
        self.cursor.execute(sql, (category_id,))
        return self.cursor.fetchone()

    def update_category(self, category):
        sql = """
              UPDATE Categories
              SET category_name   = ?, \
                  category_colour = ?, \
                  category_icon   = ?
              WHERE category_id = ? \
              """

        self.cursor.execute(sql, (
            category.category_name,
            category.category_colour,
            category.category_icon,
            category.category_id
        ))

        self.connection.commit()

    def delete_category(self, category_id):
        sql = "DELETE FROM Categories WHERE category_id = ?"

        self.cursor.execute(sql, (category_id,))
        self.connection.commit()

    # Tasks
    def add_task(self, task):
        pass

    def get_tasks(self):
        pass

    def get_task(self, task_id):
        pass

    def update_task(self, task):
        pass

    def delete_task(self, task):
        pass

class Category:
    def __init__(self, category_name, category_colour=None, category_icon=None, category_id=None):
        self.category_id = category_id
        self.category_name = category_name
        self.category_colour = category_colour
        self.category_icon = category_icon

class Task:
    def __init__(
        self,
        title,
        description,
        due_date,
        due_time,
        priority,
        importance,
        urgency,
        status,
        category_id,
        task_id=None,
        created_at=None,
        updated_at=None
    ):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.due_time = due_time
        self.priority = priority
        self.importance = importance
        self.urgency = urgency
        self.status = status
        self.category_id = category_id
        self.created_at = created_at
        self.updated_at = updated_at

db = Database()
db.create_database()
db.close()