import sqlite3

connection = sqlite3.connect("tasktracker.db")
connection.execute("PRAGMA foreign_keys = ON;")
cursor = connection.cursor()

with open("schema.sql", "r") as file:
    cursor.executescript(file.read())

connection.commit()
connection.close()

