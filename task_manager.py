

class TaskManager:
    def __init__(self, database):
        self.database = database

    def search_tasks(self,keyword):
        tasks = self.database.get_task()

        results = []

        for task in tasks:
            if keyword.lower() in task['title'].lower() or keyword.lower() in task['description'].lower():
                results.append(task)

        return results

    def sort_tasks(self, sort_by):
        tasks = self.database.get_task()

        if sort_by == "priority":
            return sorted(tasks, key=lambda task: task['priority'], reverse=True)

        if sort_by == "":

    def filter_tasks(self):
        pass

    def mark_task_completed(self):
        pass