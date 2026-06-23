import json
import os
from datetime import datetime

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

    for number, task in enumerate(tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"

        print(f"{number}. {status} {task['name']}")
        print(f"   Category: {task['category']}")
        print(f"   Priority: {task['priority']}")
        print(f"   Due Date: {task['due_date']}")
        print()


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
                if category not in categories:   # ✅ prevent duplicates
                    categories.append(category)
                print(f"Category '{category}' added ✅")
                break
            else:
                print("Please enter an existing category.")

    priority_map = {1: "High", 2: "Medium", 3: "Low"}
    while True:
        try:
            choice = int(input("Enter priority (1=High,2=Medium,3=Low): "))
            if choice in priority_map:
                priority = priority_map[choice]
                break
        except ValueError:
            pass
        print("Invalid input")

    while True:
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid format")

    task = {
        "name": task_name,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    save_tasks()   # ✅ save after adding
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