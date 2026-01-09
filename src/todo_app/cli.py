"""
Command-line interface for the Todo application
"""
import re
from typing import List, Tuple, Optional
from .storage import TodoStorage
from .models import Task


class TodoCLI:
    """
    Command-line interface handler for the Todo application.
    Parses and executes user commands.
    """

    def __init__(self, storage: TodoStorage):
        """
        Initialize the CLI with a storage instance.

        Args:
            storage (TodoStorage): The storage manager to use for operations
        """
        self.storage = storage

    def parse_command(self, user_input: str) -> Tuple[str, List[str]]:
        """
        Parse user input into command and arguments.

        Args:
            user_input (str): The raw user input

        Returns:
            Tuple[str, List[str]]: Command name and list of arguments
        """
        # Split by whitespace, but preserve quoted strings as single arguments
        # This regex matches either quoted strings or non-whitespace sequences
        pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
        matches = re.findall(pattern, user_input.strip())

        # Each match is a tuple of 3 elements, only one will be non-empty
        tokens = [match[0] or match[1] or match[2] for match in matches]

        if not tokens:
            return "help", []

        command = tokens[0].lower()
        args = tokens[1:]

        return command, args

    def execute_command(self, command: str, args: List[str]) -> str:
        """
        Execute a command with the given arguments.

        Args:
            command (str): The command to execute
            args (List[str]): Arguments for the command

        Returns:
            str: The result of the command execution
        """
        try:
            if command in ["add"]:
                return self._add_command(args)
            elif command in ["list", "ls"]:
                return self._list_command(args)
            elif command in ["update"]:
                return self._update_command(args)
            elif command in ["delete", "del"]:
                return self._delete_command(args)
            elif command in ["complete", "done"]:
                return self._complete_command(args)
            elif command in ["incomplete", "undone"]:
                return self._incomplete_command(args)
            elif command in ["help", "h"]:
                return self._help_command(args)
            elif command in ["quit", "exit", "q"]:
                return self._quit_command(args)
            else:
                return f"Unknown command: {command}. Type 'help' for available commands."
        except Exception as e:
            return f"Error: {str(e)}"

    def _add_command(self, args: List[str]) -> str:
        """
        Handle the 'add' command.

        Args:
            args (List[str]): Arguments for the add command [title, description]

        Returns:
            str: Result message
        """
        if len(args) < 1:
            return "Usage: add \"title\" [\"description\"]"

        title = args[0]
        description = args[1] if len(args) > 1 else ""

        task = self.storage.add_task(title, description)
        status_indicator = "[✓]" if task.completed else "[ ]"
        return f"Task #{task.id} added successfully: {status_indicator} {task.title} - {task.description}"

    def _list_command(self, args: List[str]) -> str:
        """
        Handle the 'list' command.

        Args:
            args (List[str]): Arguments for the list command

        Returns:
            str: Result message
        """
        if len(args) > 0:
            return "Usage: list (no arguments needed)"

        if not self.storage.has_tasks():
            return "No tasks in the list."

        tasks = self.storage.get_all_tasks()
        task_list = []
        for task in tasks:
            status_indicator = "[✓]" if task.completed else "[ ]"
            task_list.append(f"{task.id}. {status_indicator} {task.title} - {task.description}")

        return "\n".join(task_list)

    def _update_command(self, args: List[str]) -> str:
        """
        Handle the 'update' command.

        Args:
            args (List[str]): Arguments for the update command [id, title, description]

        Returns:
            str: Result message
        """
        if len(args) < 2:
            return "Usage: update <id> \"new title\" [\"new description\"]"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number, got '{args[0]}'"

        new_title = args[1]
        new_description = args[2] if len(args) > 2 else ""

        try:
            task = self.storage.update_task(task_id, new_title, new_description)
            status_indicator = "[✓]" if task.completed else "[ ]"
            return f"Task #{task.id} updated: {status_indicator} {task.title} - {task.description}"
        except Exception as e:
            return f"Error updating task: {str(e)}"

    def _delete_command(self, args: List[str]) -> str:
        """
        Handle the 'delete' command.

        Args:
            args (List[str]): Arguments for the delete command [id]

        Returns:
            str: Result message
        """
        if len(args) != 1:
            return "Usage: delete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number, got '{args[0]}'"

        try:
            self.storage.delete_task(task_id)
            return f"Task #{task_id} deleted successfully."
        except Exception as e:
            return f"Error deleting task: {str(e)}"

    def _complete_command(self, args: List[str]) -> str:
        """
        Handle the 'complete' command.

        Args:
            args (List[str]): Arguments for the complete command [id]

        Returns:
            str: Result message
        """
        if len(args) != 1:
            return "Usage: complete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number, got '{args[0]}'"

        try:
            task = self.storage.mark_task_complete(task_id)
            return f"Task #{task.id} marked as complete: [✓] {task.title}"
        except Exception as e:
            return f"Error marking task as complete: {str(e)}"

    def _incomplete_command(self, args: List[str]) -> str:
        """
        Handle the 'incomplete' command.

        Args:
            args (List[str]): Arguments for the incomplete command [id]

        Returns:
            str: Result message
        """
        if len(args) != 1:
            return "Usage: incomplete <id>"

        try:
            task_id = int(args[0])
        except ValueError:
            return f"Error: Task ID must be a number, got '{args[0]}'"

        try:
            task = self.storage.mark_task_incomplete(task_id)
            return f"Task #{task.id} marked as incomplete: [ ] {task.title}"
        except Exception as e:
            return f"Error marking task as incomplete: {str(e)}"

    def _help_command(self, args: List[str]) -> str:
        """
        Handle the 'help' command.

        Args:
            args (List[str]): Arguments for the help command

        Returns:
            str: Help text
        """
        help_text = """
Available commands:
  add "title" ["description"]    - Add a new task
  list / ls                      - View all tasks
  update <id> "title" ["desc"]   - Update a task
  delete / del <id>              - Delete a task
  complete / done <id>           - Mark task as complete
  incomplete / undone <id>       - Mark task as incomplete
  help / h                       - Show this help
  quit / exit / q                - Exit the application
        """.strip()
        return help_text

    def _quit_command(self, args: List[str]) -> str:
        """
        Handle the 'quit' command.

        Args:
            args (List[str]): Arguments for the quit command

        Returns:
            str: Result message
        """
        return "quit_application"