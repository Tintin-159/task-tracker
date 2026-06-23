from Functions import *

load_tasks()


while True:
    print("\n====== TASK MANAGER ======")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Edit Task")
    print("5. Delete Tasks")
    print("6. Exit")

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
        case 3:
            complete_task()
        case 4:
            edit_task()
        case 5:
            delete_task()
        case 6:
            break
        case _:
            print("Invalid Choice")

    input("Press Enter to Continue")