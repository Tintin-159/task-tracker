import json
import os
from datetime import datetime, date

tasks = []
categories = ["School", "Work", "Personal", "Study"]

#The functions that will be running inside the functions in the main function. 😊
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
    print("Debug...")

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

def convert_to_hours(time_input):
    time_input = time_input.lower().strip()

    try:
        value = float(time_input.split()[0])
        unit = time_input.split()[1]
    except:
        return None

    if unit in ["m", "min", "mins", "minute", "minutes"]:
        return value / 60
    elif unit in ["h", "hour", "hours"]:
        return value
    elif unit in ["d", "day", "days"]:
        return value * 24
    elif unit in ["w", "week", "weeks"]:
        return value * 24 * 7
    else:
        return None

def urgency(due_date, time_needed):
    try:
        due_datetime = datetime.strptime(tasks["due_date"], "%d-%m-%Y %H:%M")
        now = datetime.now()

        time_available = (due_datetime - now).total_seconds() / 3600
        time_needed = tasks.get("time_required", 1)

        if time_available <= 0:
            return 10

        urgency_score = (time_needed / (time_available + 1)) * 10
        return round(min(10, urgency_score), 2)

    except:
        return 0

def calculate_priority():
    pass

#sort base on the priority score to have the highest score at the top
def sort_tasks():
    pass