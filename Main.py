from Functions import *

load_tasks()


while True:
    print("\n====== TASK MANAGER ======")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a number.")
        continue

    match choice:
        case 1:
            view_tasks()
        case 2:
            add_task()
            save_tasks()
        case 3:
            complete_task()
            save_tasks()
        case 4:
            delete_task()
            save_tasks()
        case 5:
            break
        case _:
            print("Invalid Choice")

    input("Press Enter to Continue")