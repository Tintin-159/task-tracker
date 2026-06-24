import Internal_Functions as core

#The main functions
def view_tasks():
    if len(core.tasks) == 0:
        print("No Tasks Available")
        return

    now = core.datetime.now()

    for i, task in enumerate(core.tasks, start=1):
        status = "[✓]" if task["completed"] else "[ ]"

        try:
            # Parse full datetime (date + time)
            due_datetime = core.datetime.strptime(task["due_date"], "%d-%m-%Y %H:%M")
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
        print("\nAvailable categories:", ", ".join(core.categories))
        category = input("Enter category: ").strip()

        if not category:
            print("Category cannot be empty")
            continue

        category = category.capitalize()

        if category in core.categories:
            break
        else:
            choice = input("Category not found. Add it? (y/n): ").lower()

            if choice == "y":
                if category not in core.categories:
                    core.categories.append(category)
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
                due_datetime = core.datetime.strptime(due_input, fmt)
                break
            except ValueError:
                continue

        if due_datetime is None:
            print("Invalid format. Try again.")
            continue

        #If NO time was provided → set to 22:00
        if "%" not in formats[0] or due_datetime.hour == 0 and due_datetime.minute == 0:
            # Detect if user only entered date (length-based is simple + reliable here)
            if len(due_input.split()) == 1 or ":" not in due_input:
                due_datetime = due_datetime.replace(hour=22, minute=0)

        #Reject past date/time
        now = core.datetime.now()
        if due_datetime < now:
            print("Due date cannot be in the past.")
            continue

        #Store in 24-hour format
        due_date = due_datetime.strftime("%d-%m-%Y %H:%M")
        break

    #Time needed
    while True:
        time_input = input(
            "\nEnter time required (e.g. '30 min', '2 hours', '1 day', '1 week'): "
        )

        time_required = core.convert_to_hours(time_input)

        if time_required is not None and time_required > 0:
            break
        else:
            print("Invalid format. Try again.")

    urgency_value = core.urgency(due_date,time_required)
            #STORE BOTH LABEL + VALUE
    task = {
        "name": task_name,
        "category": category,
        "priority": priority,  # text label
        "value": value,        # numeric value (for sorting/graphing)
        "due_date": due_date,
        "time required": time_required,
        "urgency": urgency_value,
        "completed": False
    }

    core.tasks.append(task)
    core.save_tasks()
    print("Task added ✅")

def complete_task():
    if len(core.tasks) == 0:
        print("No Tasks Available")
        return

    view_tasks()

    try:
        choice = int(input("Enter task number: "))
    except ValueError:
        print("Invalid input")
        return

    if 1 <= choice <= len(core.tasks):
        core.tasks[choice - 1]["completed"] = True
        core.save_tasks()   # ✅ save
        print("Task marked as completed ✅")
    else:
        print("Invalid task number")

def edit_task():
    if len(core.tasks) == 0:
        print("No Tasks Available")
        return

    view_tasks()

    try:
        choice = int(input("Enter task number to edit: "))
    except ValueError:
        print("Invalid input")
        return

    if not (1 <= choice <= len(core.tasks)):
        print("Invalid task number")
        return

    task = core.tasks[choice - 1]

    print("\n--- Editing Task ---")

    #Edit name
    new_name = input(f"Enter new name (leave blank to keep '{task['name']}'): ").strip()
    if new_name:
        task["name"] = new_name

    #Edit category
    print("\nAvailable categories:", ", ".join(core.categories))
    new_category = input(f"Enter new category (leave blank to keep '{task['category']}'): ").strip()

    if new_category:
        new_category = new_category.capitalize()

        if new_category not in core.categories:
            choice = input("Category not found. Add it? (y/n): ").lower()
            if choice == "y":
                core.categories.append(new_category)

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
                due_datetime = core.datetime.strptime(due_input, fmt)
                break
            except ValueError:
                continue

        if due_datetime is None:
            print("Invalid format.")
            continue

        # If no time entered → default to 22:00
        if len(due_input.split()) <= 3:
            if ":" not in due_input:
                due_datetime = due_datetime.replace(hour=22, minute=0, second=0)
                print("No time entered → default set to 22:00")

        # Prevent past dates
        if due_datetime < core.datetime.now():
            print("Due date cannot be in the past.")
            continue

        # Store in same format as add_task
        task["due_date"] = due_datetime.strftime("%d-%m-%Y %H:%M")
        break

    # Edit time required
    while True:
        new_time = input(
            f"Enter new time required (e.g. '2 hours') or press Enter to keep: "
        ).strip()

        if not new_time:
            task["urgency"] = core.urgency(task["due_date"], task["time required"])
            break

        time_required = core.convert_to_hours(new_time)

        if time_required is not None and time_required > 0:
            task["time required"] = time_required
            task["urgency"] = core.urgency(task["due_date"], time_required)
            break
        else:
            print("Invalid format.")

    core.save_tasks()
    print("Task updated ✅")

def delete_task():
    if len(core.tasks) == 0:
        print("No Tasks Available")
        return

    view_tasks()

    try:
        choice = int(input("Enter task number: "))
    except ValueError:
        print("Invalid input")
        return

    if 1 <= choice <= len(core.tasks):
        removed = core.tasks.pop(choice - 1)
        core.save_tasks()   #save
        print(f"Task '{removed['name']}' deleted ✅")
    else:
        print("Invalid task number")

def search_task():
    if len(core.tasks) == 0:
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
        results = [t for t in core.tasks if keyword in t["name"].lower()]
    elif option == 2:
        results = [t for t in core.tasks if keyword in t["category"].lower()]
    elif option == 3:
        results = [t for t in core.tasks if keyword in t["priority"].lower()]
    elif option == 4:
        results = [
            t for t in core.tasks
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

