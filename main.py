from at_toolbox import Toolbox
from debug_helper import DebugHelper
from config_loader import load_config
from utils import display_welcome_message
from utils import clear_screen
import sys

def get_user_selection(prompt, options):
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
    for ws in workspaces:
        print(f"{ws['id']}: {ws['name']}")

def display_and_select(bases_or_tables, display_function):
    display_function(bases_or_tables)
    options = [f"{item['id']}: {item['name']}" for item in bases_or_tables]
    index = get_user_selection("Select from the above options:", options) - 1
    return bases_or_tables[index]['id'], bases_or_tables[index]['name']

def create_new_base(automator, config):
    # Retrieve and select workspace from the configuration
    if 'workspaces' in config and config['workspaces']:
        workspace_id, workspace_name = display_and_select(config['workspaces'], display_workspaces)
        print(f"Selected workspace: {workspace_name}")
    else:
        print("No workspaces configured.")
        return

    # Existing logic for base name input
    base_name = input("Enter the name of the new base: ")
    # Example of adding a default table structure
    # This can be replaced or expanded based on user input or specific requirements
    if not base_name:
        print("Base name cannot be empty.")
        return

    # User confirmation before creation
    confirmation = input(f"Are you sure you want to create a new base named '{base_name}' in '{workspace_name}'? (y/n): ")
    if confirmation.lower() != 'y':
        print("Base creation cancelled.")
        return

    # Call the function to create the new base
    base_response = automator.create_base(base_name, workspace_id)
    if base_response:
        print(f"Successfully created base with ID: {base_response['id']}")
    else:
        print("Failed to create the base. Please check the details and try again.")

def main_menu(automator, config):
    while True:
        clear_screen()
        choices = ["Create a new base", "Use a pre-existing base", "Exit"]
        choice = get_user_selection("Main Menu:", choices)

        if choice == 1:
            create_new_base(automator, config)
        elif choice == 2:
            bases = automator.list_existing_bases()
            if bases:
                base_id, _ = display_and_select(bases, automator.display_existing_bases)
                clear_screen()
                base_menu(automator, base_id)
            else:
                print("No existing bases available.")
        elif choice == 3:
            print("Goodbye!")
            break
        input("Press Enter to continue...")

def base_menu(automator, base_id):
    while True:
        clear_screen()
        choices = ["Select a table", "Return to main menu", "Exit"]
        choice = get_user_selection("", choices)

        if choice == 1:
            tables = automator.list_tables_in_base(base_id)
            if tables:
                _, table_name = display_and_select(tables, display_tables)
                clear_screen()
                table_menu(automator, base_id, table_name)
            else:
                print("No tables available to select.")
                input("Press Enter to continue...")
        elif choice == 2:
            return
        elif choice == 3:
            print("Goodbye!")
            sys.exit()

def display_tables(tables):
    print("Available Tables:")
    for idx, table in enumerate(tables, start=1):
        print(f"{idx}. {table['name']}")

def table_menu(automator, base_id, table_name):
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
    print("Select a destination base for duplication:")
    bases = automator.list_existing_bases()
    if not bases:
        print("No available bases to select as a destination.")
        return

    destination_base_id, _ = display_and_select(bases, automator.display_existing_bases)
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

    display_welcome_message()
    print()
    input("Press Enter to continue...")  # This line ensures the welcome message stays until the user proceeds
    clear_screen()  # Optional: clear the screen after the user presses Enter
    main_menu(automator, config)

if __name__ == "__main__":
    main()
