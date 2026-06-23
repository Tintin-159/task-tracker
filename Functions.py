import json
import os
from datetime import datetime, date

tasks = []
categories = ["School", "Work", "Personal", "Study"]

def load_tasks():
    global tasks, categories
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)

            # Support both old and new format
            if isinstance(data, list):
                tasks = data
            else:
                tasks = data.get("tasks", [])
                categories = data.get("categories", categories)

    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
        categories = ["School", "Work", "Personal", "Study"]


def save_tasks():
    temp_file = "tasks.json.tmp"

    data = {
        "categories": categories,
        "tasks": tasks
    }

    try:
        with open(temp_file, "w") as file:
            json.dump(data, file, indent=4)

        if os.path.exists(temp_file):
            os.replace(temp_file, "tasks.json")
        else:
            print("Error: temp file was not created.")

    except Exception as e:
        print(f"Error saving tasks: {e}")


def view_tasks():
    if len(tasks) == 0:
        print("No Tasks Available")
        return

    print("\nView Options:")
    print("1. All Tasks")
    print("2. Completed Tasks")
    print("3. Pending Tasks")

    try:
        option = int(input("Choose an option: "))
    except ValueError:
        print("Invalid input")
        return

    today = date.today()

    filtered_tasks = []

    match option:
        case 1:
            filtered_tasks = tasks
        case 2:
            filtered_tasks = [t for t in tasks if t["completed"]]
        case 3:
            filtered_tasks = [t for t in tasks if not t["completed"]]
        case _:
            print("Invalid option")
            return

    if not filtered_tasks:
        print("No tasks found for this filter.")
        return

    for i, task in enumerate(filtered_tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"

        try:
            due_date_obj = datetime.strptime(task["due_date"], "%d-%m-%Y").date()
            days_left = (due_date_obj - today).days

            if days_left < 0:
                due_text = f"OVERDUE {abs(days_left)}d"
                prefix = "🔴"
            elif days_left == 0:
                due_text = "TODAY"
                prefix = "🟠"
            elif days_left <= 2:
                due_text = f"{days_left}d"
                prefix = "🟡"
            else:
                due_text = f"{days_left}d"
                prefix = "🟢"

        except ValueError:
            due_text = "Invalid"
            prefix = "⚪"

        print(f"{i}. {prefix} {status} {task['name']} | Due: {task['due_date']} ({due_text}) | {task['category']} | {task['priority']} ({task.get('value','-')})")

def add_task():
    while True:
        task_name = input("Enter task name: ").strip()
        if task_name:
            break
        print("Task name cannot be empty")

    # Category
    while True:
        print("\nAvailable categories:", ", ".join(categories))
        category = input("Enter category: ").strip()

        if not category:
            print("Category cannot be empty")
            continue

        category = category.capitalize()

        if category in categories:
            break
        else:
            choice = input("Category not found. Add it? (y/n): ").lower()

            if choice == "y":
                if category not in categories:
                    categories.append(category)
                print(f"Category '{category}' added ✅")
                break
            else:
                print("Please enter an existing category.")

    # ✅ NEW IMPORTANCE SYSTEM
    while True:
        try:
            value = int(input(
                "\nEnter importance value (1–10):\n"
                "9–10 → Critical\n"
                "7–8 → Very Important\n"
                "5–6 → Moderate\n"
                "3–4 → Low\n"
                "1–2 → Almost No Value\n"
                "Your input: "
            ))

            if 1 <= value <= 10:
                if value >= 9:
                    priority = "Critical"
                elif value >= 7:
                    priority = "Very Important"
                elif value >= 5:
                    priority = "Moderate"
                elif value >= 3:
                    priority = "Low"
                else:
                    priority = "Almost No Value"
                break
            else:
                print("Please enter a number between 1 and 10.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    # Due date
    while True:
        due_input = input("\nEnter due date (DD-MM-YYYY or DD MM YYYY): ").strip()

        formats = ["%d-%m-%Y", "%d %m %Y"]

        due_date_obj = None

        try:
            # ✅ Try both formats
            for fmt in formats:
                try:
                    due_date_obj = datetime.strptime(due_input, fmt).date()
                    break
                except ValueError:
                    continue

            # ❌ If no format worked
            if due_date_obj is None:
                print("Invalid format. Use DD-MM-YYYY or DD MM YYYY.")
                continue

            # ✅ Get today's date
            today = date.today()

            # ❌ Reject past dates
            if due_date_obj < today:
                print("Due date cannot be in the past.")
                continue

            # ✅ Store in consistent format
            due_date = due_date_obj.strftime("%d-%m-%Y")
            break

        except Exception:
            print("Invalid input. Please try again.")

    # ✅ STORE BOTH LABEL + VALUE
    task = {
        "name": task_name,
        "category": category,
        "priority": priority,  # text label
        "value": value,        # numeric value (for sorting/graphing)
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    save_tasks()
    print("Task added ✅")


def complete_task():
    if len(tasks) == 0:
        print("No Tasks Available")
        return

    view_tasks()

    try:
        choice = int(input("Enter task number: "))
    except ValueError:
        print("Invalid input")
        return

    if 1 <= choice <= len(tasks):
        tasks[choice - 1]["completed"] = True
        save_tasks()   # ✅ save
        print("Task marked as completed ✅")
    else:
        print("Invalid task number")

def edit_task():
    if len(tasks) == 0:
        print("No Tasks Available")
        return

    view_tasks()

    try:
        choice = int(input("Enter task number to edit: "))
    except ValueError:
        print("Invalid input")
        return

    if not (1 <= choice <= len(tasks)):
        print("Invalid task number")
        return

    task = tasks[choice - 1]

    print("\n--- Editing Task ---")

    # ✅ Edit name
    new_name = input(f"Enter new name (leave blank to keep '{task['name']}'): ").strip()
    if new_name:
        task["name"] = new_name

    # ✅ Edit category
    print("\nAvailable categories:", ", ".join(categories))
    new_category = input(f"Enter new category (leave blank to keep '{task['category']}'): ").strip()

    if new_category:
        new_category = new_category.capitalize()

        if new_category not in categories:
            choice = input("Category not found. Add it? (y/n): ").lower()
            if choice == "y":
                categories.append(new_category)

        task["category"] = new_category

    # ✅ Edit importance
    while True:
        new_value_input = input(f"Enter new importance value (1–10) or press Enter to keep ({task.get('value','-')}): ").strip()

        if not new_value_input:
            break

        try:
            value = int(new_value_input)
            if 1 <= value <= 10:

                if value >= 9:
                    priority = "Critical"
                elif value >= 7:
                    priority = "Very Important"
                elif value >= 5:
                    priority = "Moderate"
                elif value >= 3:
                    priority = "Low"
                else:
                    priority = "Almost No Value"

                task["value"] = value
                task["priority"] = priority
                break
            else:
                print("Enter a number between 1–10.")
        except ValueError:
            print("Invalid input.")

    # ✅ Edit due date
    from datetime import datetime, date

    while True:
        due_input = input(f"Enter new due date (DD-MM-YYYY) or press Enter to keep ({task['due_date']}): ").strip()

        if not due_input:
            break

        formats = ["%d-%m-%Y", "%d %m %Y"]
        due_date_obj = None

        for fmt in formats:
            try:
                due_date_obj = datetime.strptime(due_input, fmt).date()
                break
            except ValueError:
                continue

        if due_date_obj is None:
            print("Invalid format.")
            continue

        if due_date_obj < date.today():
            print("Due date cannot be in the past.")
            continue

        task["due_date"] = due_date_obj.strftime("%d-%m-%Y")
        break

    save_tasks()
    print("Task updated ✅")

def delete_task():
    if len(tasks) == 0:
        print("No Tasks Available")
        return

    view_tasks()

    try:
        choice = int(input("Enter task number: "))
    except ValueError:
        print("Invalid input")
        return

    if 1 <= choice <= len(tasks):
        removed = tasks.pop(choice - 1)
        save_tasks()   # ✅ save
        print(f"Task '{removed['name']}' deleted ✅")
    else:
        print("Invalid task number")