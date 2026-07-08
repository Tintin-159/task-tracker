# Database Design

## Tasks Table

| Field | Data Type | Description |
|-------|-----------|-------------|
| task_id | INTEGER | Primary Key |
| title | TEXT | Task title |
| description | TEXT | Task description |
| due_date | DATE | Due date |
| due_time | TIME | Due time |
| priority | INTEGER | Priority (1–10) |
| status | TEXT | To Do, In Progress, Completed |
| category_id | INTEGER | Foreign Key to Categories |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last updated timestamp |

## Categories Table

| Field | Data Type | Description |
|-------|-----------|-------------|
| category_id | INTEGER | Primary Key |
| category_name | TEXT | Category name |
| category_colour | TEXT | Display colour |
| category_icon | TEXT | Display icon |

## Relationships

- One Category can have many Tasks.
- Each Task belongs to one Category.