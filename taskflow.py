import os
import json
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize Colorama for color-coded output
init(autoreset=True)

TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"


# --- Task Management Class ---
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                self.tasks = json.load(file)
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, description, category, priority, deadline=None):
        """Add a new task."""
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "category": category,
            "priority": priority,
            "deadline": deadline,
            "completed": False,
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"{Fore.GREEN}Task added successfully!{Style.RESET_ALL}")

    def view_tasks(self, filter_by=None, sort_by=None):
        """View tasks with optional filtering and sorting."""
        tasks = self.tasks

        if filter_by:
            tasks = [task for task in tasks if task["category"] == filter_by]

        if sort_by == "priority":
            # Sort by priority (High > Medium > Low)
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            tasks = sorted(tasks, key=lambda x: priority_order.get(x["priority"], 3))
        elif sort_by == "deadline":
            tasks = sorted(tasks, key=lambda x: x["deadline"] or "9999-12-31")

        if not tasks:
            print(f"{Fore.YELLOW}No tasks found.{Style.RESET_ALL}")
            return

        # Create the table with a pastel background for indexing title
        headers = ["ID", "Description", "Category", "Priority", "Deadline", "Status"]
        table = []

        for task in tasks:
            status = "✔" if task["completed"] else "✘"
            table.append(
                [task["id"], task["description"], task["category"], task["priority"], task["deadline"], status])

        # Table formatting with pastel header and white background for content
        table_output = tabulate(table, headers=headers, tablefmt="fancy_grid", stralign="center")

        # Adding pastel background to header manually (you can adjust colors)
        pastel_header = f"{Fore.MAGENTA}{Style.BRIGHT}" + "╔═" + "═" * 48 + "═╗" + "\n"
        pastel_header += f"{Fore.MAGENTA}{Style.BRIGHT}" + "║ " + "   ID   " + "  ║  Description  ║  Category  ║ Priority ║ Deadline ║ Status ║" + "\n"
        pastel_header += f"{Fore.MAGENTA}{Style.BRIGHT}" + "╚═" + "═" * 48 + "═╝"

        print(f"{pastel_header}")
        print(f"{Fore.WHITE}{table_output}{Style.RESET_ALL}")

    def edit_task(self, task_id, **kwargs):
        """Edit an existing task."""
        for task in self.tasks:
            if task["id"] == task_id:
                task.update({k: v for k, v in kwargs.items() if v is not None})
                self.save_tasks()
                print(f"{Fore.GREEN}Task updated successfully!{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}Task ID not found.{Style.RESET_ALL}")

    def delete_task(self, task_id):
        """Delete a task and adjust the IDs of subsequent tasks."""
        # Remove the task with the specified task_id
        self.tasks = [task for task in self.tasks if task["id"] != task_id]

        # Adjust task IDs for remaining tasks
        for i, task in enumerate(self.tasks):
            task["id"] = i + 1  # Reassign IDs to ensure they are contiguous

        # Save the updated list of tasks
        self.save_tasks()
        print(f"{Fore.GREEN}Task deleted successfully! IDs have been updated.{Style.RESET_ALL}")

    def mark_task_complete(self, task_id):
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                print(f"{Fore.GREEN}Task marked as completed!{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}Task ID not found.{Style.RESET_ALL}")


# --- User Authentication Functions ---
def load_users():
    """Load users from the JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return []


def save_users(users):
    """Save users to the JSON file."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


def authenticate_user():
    """Authenticate the user by checking username and password."""
    users = load_users()

    # Improved login screen formatting
    print(f"{Fore.BLUE}\n{'=' * 50}")
    print(f"{' ' * 12}Welcome to TaskFlow!{' ' * 12}")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")

    username = input("Enter your Username/ID: ").strip()
    password = input("Enter your Password: ").strip()

    # Check if user exists and password matches
    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"{Fore.GREEN}\n{'=' * 50}")
            print(f"{' ' * 14}Login successful!{' ' * 14}")
            print(f"{'=' * 50}{Style.RESET_ALL}")
            return username

    print(f"{Fore.RED}\n{'=' * 50}")
    print(f"{' ' * 12}Invalid username or password.{Style.RESET_ALL}")
    print(f"{'=' * 50}")
    return None


def register_user():
    """Register a new user."""
    users = load_users()

    print(f"{Fore.YELLOW}\n{'=' * 50}")
    print(f"{' ' * 12}Welcome to the registration page!{' ' * 12}")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")

    username = input("Enter a new Username/ID: ").strip()
    password = input("Enter a new Password: ").strip()

    # Check if the username already exists
    for user in users:
        if user["username"] == username:
            print(f"{Fore.RED}Username already exists. Please try again.{Style.RESET_ALL}")
            return None

    # Add the new user to the users list
    users.append({"username": username, "password": password})
    save_users(users)
    print(f"{Fore.GREEN}\nHurray!! Your Registration has been completed!")
    print(f"{Fore.GREEN}Please log in to continue.{Style.RESET_ALL}")

    # Ask for login after registration
    return authenticate_user()


# --- User Interface ---
def display_menu():
    print(
        f"{Fore.MAGENTA}{' ' * 3}╔════════════════════ WELCOME TO TASKFLOW MANAGEMENT SYSTEM ════════════════════{' ' * 3}{Style.RESET_ALL}")

    # Unique subheading with a different border and color
    print(
        f"{Fore.CYAN}{' ' * 5}            ╔══════════ DEVELOPED BY TEAM ATNS ════════════════════════{' ' * 5}{Style.RESET_ALL}")

    # Menu options in a structured and aligned way
    print(f"{Fore.GREEN}\n╔═══════════════════════════════════════════════════════════════════════════╗")
    print(f"{' ' * 10}1. Add Task")
    print(f"{' ' * 10}2. View Tasks")
    print(f"{' ' * 10}3. Edit Task")
    print(f"{' ' * 10}4. Delete Task")
    print(f"{' ' * 10}5. Mark Task as Complete")
    print(f"{' ' * 10}6. Filter Tasks by Category")
    print(f"{' ' * 10}7. Sort Tasks")
    print(f"{' ' * 10}8. Exit")
    print(f"╚═══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")


def input_category():
    """Prompt the user to select a category with validation."""
    while True:
        print("\nSelect Task Category:")
        print("1. Work")
        print("2. Personal")
        print("3. University")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "Work"
        elif choice == "2":
            return "Personal"
        elif choice == "3":
            return "University"
        elif choice.isdigit():
            print(
                f"{Fore.RED}You have entered a wrong keyword or please enter a number! within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}You have entered a wrong keyword or please enter a number! within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")


def input_priority():
    """Prompt the user to select priority with validation."""
    while True:
        print("\nSelect Task Priority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "High"
        elif choice == "2":
            return "Medium"
        elif choice == "3":
            return "Low"
        elif choice.isdigit():
            print(
                f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")


def input_date():
    """Prompt the user to enter a valid date (YYYY-MM-DD) or leave blank to skip."""
    while True:
        deadline = input("Deadline (YYYY-MM-DD, optional): ").strip()
        if not deadline:  # User chooses to leave the field empty
            return None
        try:
            # Check if the input matches the required date format
            entered_date = datetime.strptime(deadline, "%Y-%m-%d")

            # Check if the entered date is in the past
            if entered_date < datetime.now():
                print(f"{Fore.RED}The date you have entered has already passed, please enter a future date.{Style.RESET_ALL}")
                continue

            return deadline
        except ValueError:
            print(f"{Fore.RED}Please enter a date in the format YYYY-MM-DD, or hit Enter to continue.{Style.RESET_ALL}")


def input_sort_option():
    """Prompt the user to choose sorting option with validation."""
    while True:
        print("\nSort Tasks By:")
        print("1. Priority")
        print("2. Deadline")
        print("3. None")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "priority"
        elif choice == "2":
            return "deadline"
        elif choice == "3":
            return None
        elif choice.isdigit():
            print(
                f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")


def return_to_home():
    """Display a 'Return to Home' option to go back to the main menu."""
    input(f"{Fore.CYAN}\n--- Press Enter to return to Home Menu ---{Style.RESET_ALL}")


def main():
    print(f"{Fore.CYAN}\nWelcome to TaskFlow! Please select an option:")
    print(f"{Fore.GREEN}1. Log in")
    print(f"{Fore.YELLOW}2. Register new user")
    choice = input(f"{Fore.CYAN}Enter your choice (1-2): ").strip()

    if choice == "1":
        username = authenticate_user()
        if username is None:
            print(f"{Fore.RED}Exiting TaskFlow. Goodbye!{Style.RESET_ALL}")
            return
    elif choice == "2":
        username = register_user()
        if username is None:
            print(f"{Fore.RED}Exiting TaskFlow. Goodbye!{Style.RESET_ALL}")
            return
    else:
        print(f"{Fore.RED}Invalid choice! Exiting TaskFlow for security reason.{Style.RESET_ALL}")
        return

    task_manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            description = input("Task Description: ").strip()
            category = input_category()
            priority = input_priority()
            deadline = input_date()
            task_manager.add_task(description, category, priority, deadline)
            return_to_home()  # Return to home after adding the task

        elif choice == "2":
            sort_option = input_sort_option()
            task_manager.view_tasks(sort_by=sort_option)
            return_to_home()

        elif choice == "3":
            task_manager.view_tasks()  # Display all tasks before asking for the task ID

            task_id = input("Enter Task ID to edit: ").strip()

            if not task_id.isdigit():
                print(
                    f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")
                return

            task_id = int(task_id)
            description = input("New Task Description (leave empty to keep current): ").strip()
            category = input_category()
            priority = input_priority()
            deadline = input_date()

            task_manager.edit_task(task_id, description=description, category=category, priority=priority,
                                   deadline=deadline)

            return_to_home()

        elif choice == "4":
            task_manager.view_tasks()  # Display all tasks before asking for the task ID

            task_id = input("Enter Task ID to delete: ").strip()

            if not task_id.isdigit():
                print(
                    f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")
                return

            task_id = int(task_id)
            task_manager.delete_task(task_id)

            return_to_home()

        elif choice == "5":
            task_manager.view_tasks()  # Display all tasks before asking for the task ID

            task_id = input("Enter Task ID to mark as completed: ").strip()

            if not task_id.isdigit():
                print(
                    f"{Fore.RED}You have entered a wrong keyword or please enter a number within range\n {Fore.MAGENTA}Thank you Professor Hamdi for making us aware of this error!{Style.RESET_ALL}")
                return

            task_id = int(task_id)
            task_manager.mark_task_complete(task_id)

            return_to_home()

        elif choice == "6":
            category = input_category()
            task_manager.view_tasks(filter_by=category)
            return_to_home()

        elif choice == "7":
            sort_option = input_sort_option()
            task_manager.view_tasks(sort_by=sort_option)
            return_to_home()

        elif choice == "8":
            print(f"{Fore.RED}Goodbye! See You Again Soon {Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
