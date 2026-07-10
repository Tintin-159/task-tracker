from database import Database
from task_manager import TaskManager

def main():
    db = Database()
    db.create_database()

    tm = TaskManager()

    # Program starts here

    db.close()

if __name__ == '__main__':
    main()