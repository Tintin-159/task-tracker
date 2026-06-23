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

    now = datetime.now()

    for i, task in enumerate(tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"

        try:
            # Parse full datetime (date + time)
            due_datetime = datetime.strptime(task["due_date"], "%d-%m-%Y %H:%M")
            time_left = due_datetime - now

            total_seconds = int(time_left.total_seconds())

            if total_seconds < 0:
                days = abs(total_seconds) // 86400
                hours = (abs(total_seconds) % 86400) // 3600
                due_text = f"OVERDUE {days}d {hours}h"
                prefix = "🔴"

            else:
                days = total_seconds // 86400
                hours = (total_seconds % 86400) // 3600

                if days == 0 and hours == 0:
                    due_text = "NOW"
                    prefix = "🟠"
                elif days == 0:
                    due_text = f"{hours}h"
                    prefix = "🟠"
                elif days <= 2:
                    due_text = f"{days}d {hours}h"
                    prefix = "🟡"
                else:
                    due_text = f"{days}d"
                    prefix = "🟢"

        except ValueError:
            due_text = "Invalid"
            prefix = "⚪"

        print(
            f"{i}. {prefix} {status} {task['name']} | Due: {task['due_date']} ({due_text}) | {task['category']} | {task['priority']} ({task.get('value', '-')})"
        )

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

    #NEW IMPORTANCE SYSTEM
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
        due_input = input(
            "\nEnter due date (DD-MM-YYYY or DD MM YYYY)\n"
            "Optional time (24h): DD-MM-YYYY HH:MM\n> "
        ).strip()

        formats = [
            "%d-%m-%Y %H:%M",
            "%d %m %Y %H:%M",
            "%d-%m-%Y",
            "%d %m %Y"
        ]

        due_datetime = None

        # Try all formats
        for fmt in formats:
            try:
                due_datetime = datetime.strptime(due_input, fmt)
                break
            except ValueError:
                continue

        if due_datetime is None:
            print("Invalid format. Try again.")
            continue

        # ✅ If NO time was provided → set to 22:00
        if "%" not in formats[0] or due_datetime.hour == 0 and due_datetime.minute == 0:
            # Detect if user only entered date (length-based is simple + reliable here)
            if len(due_input.split()) == 1 or ":" not in due_input:
                due_datetime = due_datetime.replace(hour=22, minute=0)

        # ✅ Reject past date/time
        now = datetime.now()
        if due_datetime < now:
            print("Due date cannot be in the past.")
            continue

        # ✅ Store in 24-hour format
        due_date = due_datetime.strftime("%d-%m-%Y %H:%M")
        break


    #STORE BOTH LABEL + VALUE
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

    #Edit name
    new_name = input(f"Enter new name (leave blank to keep '{task['name']}'): ").strip()
    if new_name:
        task["name"] = new_name

    #Edit category
    print("\nAvailable categories:", ", ".join(categories))
    new_category = input(f"Enter new category (leave blank to keep '{task['category']}'): ").strip()

    if new_category:
        new_category = new_category.capitalize()

        if new_category not in categories:
            choice = input("Category not found. Add it? (y/n): ").lower()
            if choice == "y":
                categories.append(new_category)

        task["category"] = new_category

    #Edit importance
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

    #Edit due date

    while True:
        due_input = input(
            f"Enter new due date (DD-MM-YYYY + optional HH:MM)\n"
            f"Leave blank to keep ({task['due_date']}): "
        ).strip()

        if not due_input:
            break

        formats = [
            "%d-%m-%Y %H:%M",
            "%d %m %Y %H:%M",
            "%d-%m-%Y",
            "%d %m %Y"
        ]

        due_datetime = None

        for fmt in formats:
            try:
                due_datetime = datetime.strptime(due_input, fmt)
                break
            except ValueError:
                continue

        if due_datetime is None:
            print("Invalid format.")
            continue

        # If no time entered → default to 22:00
        if len(due_input.split()) <= 3:
            due_datetime = due_datetime.replace(hour=22, minute=0, second=0)
            print("No time entered → default set to 22:00")

        # Prevent past dates
        if due_datetime < datetime.now():
            print("Due date cannot be in the past.")
            continue

        # Store in same format as add_task
        task["due_date"] = due_datetime.strftime("%d-%m-%Y %H:%M")
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

def search_task():
    if len(tasks) == 0:
        print("No Tasks Available")
        return

    print("\nSearch By:")
    print("1. Name")
    print("2. Category")
    print("3. Importance")
    print("4. Search All")

    try:
        option = int(input("Choose an option: "))
    except ValueError:
        print("Invalid input")
        return

    keyword = input("Enter keyword: ").strip().lower()

    if not keyword:
        print("Search cannot be empty.")
        return

    #Filtering logic
    if option == 1:
        results = [t for t in tasks if keyword in t["name"].lower()]
    elif option == 2:
        results = [t for t in tasks if keyword in t["category"].lower()]
    elif option == 3:
        results = [t for t in tasks if keyword in t["priority"].lower()]
    elif option == 4:
        results = [
            t for t in tasks
            if keyword in t["name"].lower()
            or keyword in t["category"].lower()
            or keyword in t["priority"].lower()
        ]
    else:
        print("Invalid option")
        return

    if not results:
        print("No matching tasks found.")
        return

    print(f"\nFound {len(results)} result(s):\n")

    from datetime import datetime, date
    today = date.today()

    #one-line display style
    for i, task in enumerate(results, start=1):
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


def filter_task():
    pass