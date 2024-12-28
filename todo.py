import argparse
import json
import os

# File to store tasks
TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(args):
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "task": args.task, "completed": False})
    save_tasks(tasks)
    print(f"Task added: {args.task}")

def list_tasks(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks available.")
    else:
        print("Tasks:")
        for task in tasks:
            status = "✔" if task["completed"] else "✘"
            print(f"{task['id']}: {task['task']} [{status}]")

def update_task(args):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.id:
            task["task"] = args.task
            save_tasks(tasks)
            print(f"Task {args.id} updated to: {args.task}")
            return
    print(f"Task with ID {args.id} not found.")

def delete_task(args):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != args.id]
    save_tasks(tasks)
    print(f"Task {args.id} deleted.")

def mark_complete(args):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {args.id} marked as complete.")
            return
    print(f"Task with ID {args.id} not found.")

def main():
    parser = argparse.ArgumentParser(description="To-Do List Manager")
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    
    # Add task
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("task", type=str, help="The task description")
    parser_add.set_defaults(func=add_task)
    
    # List tasks
    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.set_defaults(func=list_tasks)
    
    # Update task
    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("id", type=int, help="The task ID")
    parser_update.add_argument("task", type=str, help="The new task description")
    parser_update.set_defaults(func=update_task)
    
    # Delete task
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="The task ID")
    parser_delete.set_defaults(func=delete_task)
    
    # Mark task as complete
    parser_complete = subparsers.add_parser("complete", help="Mark a task as complete")
    parser_complete.add_argument("id", type=int, help="The task ID")
    parser_complete.set_defaults(func=mark_complete)
    
    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
