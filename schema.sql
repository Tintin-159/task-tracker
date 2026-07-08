CREATE TABLE Tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL ,
    description TEXT,
    due_date DATE,
    due_time TIME,
    priority INTEGER NOT NULL,
    status TEXT NOT NULL,
    category_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Categories (
    category_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    category_colour TEXT,
    category_icon TEXT
)