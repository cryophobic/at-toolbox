from at_toolbox import Toolbox
from debug_helper import DebugHelper
from config_loader import load_config
from utils import display_welcome_message
from utils import clear_screen
import sys

def get_user_selection(prompt, options):
    """
    Presents a menu to the user and gets their selection.

    This function displays a prompt and a list of options to the user, then returns the user's choice.

    Args:
        prompt (str): The message to display to the user.
        options (list): A list of options for the user to choose from.

    Returns:
        int: The index of the user's selection from the options list.
    """
    while True:
        print(prompt)
        print()
        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")
        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid selection. Please enter a number within the list range.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def display_workspaces(workspaces):
    """
    Displays a list of workspaces.

    Args:
        workspaces (list): A list of workspace dictionaries, each containing 'id' and 'name'.
    """
    for ws in workspaces:
        print(f"{ws['id']}: {ws['name']}")

def display_and_select(items, format_function):
    """
    Displays a list of items (bases, tables, etc.) and allows the user to select one.

    Args:
        items (list): A list of items to display and choose from.
        format_function (function): Function to format the display of each item.

    Returns:
        tuple: The selected item's ID and name, or (None, None) if no items.
    """
    if not items:
        print("No items available.")
        return None, None

    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {format_function(item)}")

    options = [format_function(item) for item in items]
    index = get_user_selection("Select from the above options:", options) - 1
    return items[index]['id'], items[index]['name']

def create_new_base(automator, config):
    """
    Guides the user through the process of creating a new base.

    Args:
        automator (Toolbox): An instance of the Toolbox class for interacting with the API.
        config (dict): Configuration settings, including workspaces.
    """
    # Retrieve and select workspace from the configuration
    workspaces = config.get('workspaces', [])
    if len(workspaces) == 1:
        workspace_id, workspace_name = workspaces[0]['id'], workspaces[0]['name']
        clear_screen()
        print(f"Workspace: {workspace_name}")
        print()
    elif len(workspaces) > 1:
        workspace_id, workspace_name = display_and_select(workspaces, lambda workspace: workspace['name'])
        print(f"Workspace: {workspace_name}")
        print()
    else:
        print("No workspaces configured.")
        return

    # Fetch the list of existing bases
    bases = automator.list_existing_bases()

    # Existing logic for base name input
    base_name = input("Enter the name of the new base: ")
    clear_screen()
    # Example of adding a default table structure
    # This can be replaced or expanded based on user input or specific requirements
    if not base_name:
        print(f"Workspace: {workspace_name}")
        print()
        print("Base name cannot be empty.")
        return

    # User confirmation before creation
    print(f"Workspace: {workspace_name}")
    print()   
    confirmation = input(f"Are you sure you want to create a new base named '{base_name}' in '{workspace_name}'? (y/n): ")
    clear_screen()
    if confirmation.lower() != 'y':
        print("Base creation cancelled.")
        print()
        return

    # Call the function to create the new base
    base_response = automator.create_base(base_name, workspace_id)
    if base_response:
        print(f"Workspace: {workspace_name}")
        print()
        print(f"Successfully created base with ID: {base_response['id']}")
        print()
    else:
        print(f"Workspace: {workspace_name}")
        print()
        print("Failed to create the base. Please check the details and try again.")
        print()

def main_menu(automator, bases, config):
    """
    Presents the main menu and handles user interaction for the initial options.

    Args:
        automator (Toolbox): An instance of the Toolbox class for API interactions.
        bases (list): A list of existing bases.
        config (dict): The configuration settings for the application.
    """
    while True:
        clear_screen()
        choices = ["Create a new base", "Use a pre-existing base", "Exit"]
        choice = get_user_selection("Main Menu:", choices)

        if choice == 1:
            create_new_base(automator, config)
        elif choice == 2:
            if bases:
                base_name = display_and_select(bases, lambda base: base['name'])
                if base_name:
                    base_id = next((base['id'] for base in bases if base['name'] == base_name), None)
                    clear_screen()
                    base_menu(automator, base_id)
                else:
                    print("Invalid base selection.")
            else:
                print("No existing bases available.")
        elif choice == 3:
            print()
            clear_screen()
            print("Goodbye!")

            break
        input("Press Enter to continue...")

def base_menu(automator, base_id):
    """
    Presents the base menu and handles user interactions for base-specific options.

    Args:
        automator (Toolbox): An instance of the Toolbox class for API interactions.
        base_id (str): The ID of the selected base.
    """
    while True:
        clear_screen()
        choices = ["Select a table", "Return to main menu", "Exit"]
        choice = get_user_selection(f"'{base_id}' Base Menu:", choices)

        if choice == 1:
            tables = automator.list_tables_in_base(base_id)
            if tables:
                display_tables(tables)
                table_name = select_table(tables)
                if table_name:
                    clear_screen()
                    table_menu(automator, base_id, table_name)
                else:
                    print("Invalid table selection.")
            else:
                print("No tables available to select.")
            input("Press Enter to continue...")
        elif choice == 2:
            return
        elif choice == 3:
            clear_screen()
            print()
            print("Goodbye!")
            sys.exit()

def display_tables(tables):
    """
    Displays a list of tables in a user-friendly format.

    Args:
        tables (list): A list of tables, each represented as a dictionary with 'name'.
    """
    if not tables:
        print("No tables available.")
    else:
        print("Available Tables:")
        for idx, table in enumerate(tables, start=1):
            print(f"{idx}. {table['name']}")

def select_table(tables):
    """
    Allows the user to select a table from a list.

    Args:
        tables (list): A list of tables, each represented as a dictionary.

    Returns:
        str: The name of the selected table, or None if the selection is invalid.
    """
    if not tables:
        return None

    while True:
        try:
            choice = int(input("Enter the numeric value of the table you would like to select: "))
            if choice in range(1, len(tables) + 1):
                return tables[choice - 1]["name"]
            else:
                print("Invalid selection. Please enter a numeric value within the list range.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def table_menu(automator, base_id, table_name):
    """
    Presents the table menu and handles user interactions for table-specific options.

    Args:
        automator (Toolbox): An instance of the Toolbox class for API interactions.
        base_id (str): The ID of the base containing the table.
        table_name (str): The name of the selected table.
    """
    while True:
        clear_screen()
        choices = ["Duplicate to another base", "Return to main menu", "Exit"]
        choice = get_user_selection(f"'{table_name}' Table Menu:", choices)

        if choice == 1:
            duplicate_table_to_another_base(automator, base_id, table_name)
        elif choice == 2:
            return
        elif choice == 3:
            print("Goodbye!")
            sys.exit()

def duplicate_table_to_another_base(automator, source_base_id, table_name):
    """
    Facilitates the process of duplicating a table to another base.

    Args:
        automator (Toolbox): An instance of the Toolbox class for API interactions.
        source_base_id (str): The ID of the base containing the source table.
        table_name (str): The name of the table to duplicate.
    """
    print("Select a destination base for duplication:")
    bases = automator.list_existing_bases()
    if not bases:
        print("No available bases to select as a destination.")
        return

    destination_base_id = display_and_select(bases, lambda base: f"{base['id']}: {base['name']}")
    tables = automator.get_tables(source_base_id)
    structure = next((table for table in tables if table["name"] == table_name), None)
    if not structure:
        print(f"Table '{table_name}' not found in source base.")
        return

    fields = [{'name': field['name'], 'type': field['type']} for field in structure['fields']]
    create_response = automator.create_table_with_structure(destination_base_id, table_name, fields)
    if not create_response:
        print(f"Failed to create table '{table_name}' in destination base.")
        return

    records = automator.get_records(source_base_id, table_name)
    if records:
        automator.insert_records_into_table(destination_base_id, table_name, records)
        print(f"Table '{table_name}' duplicated to base ID {destination_base_id}.")
    else:
        print(f"No records found in table '{table_name}' or failed to fetch records.")

def main():
    """
    The main function that serves as the entry point of the utility.

    This function orchestrates the overall workflow of the application, handling initialization, user interactions, and execution of main functionalities.
    """
    config = load_config()
    automator = Toolbox(config['api_key'])
    #debugger = DebugHelper(config['api_key'])

        # Construct the data for the request
    # data = {
        # "name": "Apartment Hunting",
        # "tables": [
            # {
                # "description": "A to-do list of places to visit",
                # "fields": [
                    # {
                        # "description": "Name of the apartment",
                        # "name": "Name",
                        # "type": "singleLineText"
                    # },
                    # {
                        # "name": "Address",
                        # "type": "singleLineText"
                    # },
                    # {
                        # "name": "Visited",
                        # "options": {
                            # "color": "greenBright",
                            # "icon": "check"
                        # },
                        # "type": "checkbox"
                    # }
                # ],
                # "name": "Apartments"
            # }
        # ],
        # "workspaceId": config['workspaces'][0]['id']  # Assuming your workspace ID is stored in config
    # }


    # Use the debugger to make an API request and log the details:
    #response = debugger.make_debug_api_request("POST", "https://api.airtable.com/v0/meta/bases", data=data)

    bases = automator.list_existing_bases()  # Fetch the list of existing bases
    display_welcome_message()
    print()
    input("Press Enter to continue...")  # This line ensures the welcome message stays until the user proceeds
    clear_screen()  # Optional: clear the screen after the user presses Enter
    main_menu(automator, bases, config)  # Pass the list of bases to the main_menu function

if __name__ == "__main__":
    main()
