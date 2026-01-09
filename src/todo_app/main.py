"""
Main entry point for the Todo application
"""
from .storage import TodoStorage
from .cli import TodoCLI


def main():
    """
    Main application loop for the Todo console application.
    """
    print("Welcome to the In-Memory Todo Console Application!")
    print("Type 'help' for available commands or 'quit' to exit.\n")

    # Initialize storage and CLI
    storage = TodoStorage()
    cli = TodoCLI(storage)

    # Main application loop
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()

            # Skip empty input
            if not user_input:
                continue

            # Parse and execute the command
            command, args = cli.parse_command(user_input)
            result = cli.execute_command(command, args)

            # Check if the command was to quit
            if result == "quit_application":
                print("Goodbye!")
                break

            # Print the result
            print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()