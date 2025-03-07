import json
import typer
from rich import print

app = typer.Typer()
TASKS_FILE = "tasks.json"


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

tasks = load_tasks()

@app.command()
def add(description):
    tasks.append({"description": description, "completed": False})
    save_tasks(tasks)
    print(f"[green]✅ Task added successfully:[/green] {description}")

@app.command()
def view():
    if not tasks:
        print("[yellow]⚠️ No tasks available. Add a new task to get started![/yellow]")
        return

    print("\n[bold cyan]📌 Your To-Do List:[/bold cyan]")
    for idx, task in enumerate(tasks, 1):
        status = "✅" if task["completed"] else "❌"
        print(f"{idx}. {status} {task['description']}")

@app.command()
def complete(task_number):
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        save_tasks(tasks)
        print(f"[bold green]🎉 Task {task_number} marked as completed![/bold green]")
    else:
        print("[red]❌ Invalid task number. Please enter a valid number.[/red]")

@app.command()
def remove(task_number):
    if 1 <= task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"[red]🗑️  Task removed successfully:[/red] {removed_task['description']}")
    else:
        print("[red]❌ Invalid task number. Please enter a valid number.[/red]")


if __name__ == "__main__":
    app()
