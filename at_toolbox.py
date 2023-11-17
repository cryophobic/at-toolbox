import requests

class Toolbox:
    """
    This class provides methods to interact with the Airtable API.

    Attributes:
        api_base (str): Base URL for the Airtable API.
        headers (dict): Headers to include in API requests, including the authorization token.

    Methods:
        create_base: Creates a new base in a specified workspace.
        list_existing_bases: Retrieves a list of existing bases.
        display_existing_bases: Displays the existing bases in a user-friendly format.
        select_existing_base: Allows the user to select an existing base.
        list_tables_in_base: Fetches and displays tables from a specified base.
        get_tables: Fetches tables and their structure from a base.
        get_records: Fetches all records from a specified table.
        create_table_with_structure: Creates a new table with a given structure in a base.
        get_table_structure: Fetches the structure of a specified table.
        get_records_from_table: Fetches all records from a specified table.
        insert_records_into_table: Inserts records into a specified table.
    """

    def __init__(self, api_key):
        """
        Initializes the Toolbox with the given API key.

        Args:
            api_key (str): The API key used for authenticating with the Airtable API.
        """
        self.api_base = "https://api.airtable.com/v0"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_api_request(self, method, endpoint, data=None):
        """
        Makes an API request to the Airtable API.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to request.
            data (dict, optional): Data to be sent in the body of the request for POST requests.

        Returns:
            dict: The JSON response from the API, or None if there was an error.
        """
        url = f"{self.api_base}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            # Handle errors here, for example:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def create_base(self, base_name, workspace_id):
        """
        Creates a new base in the specified workspace.

        Args:
            base_name (str): The name of the new base to create.
            workspace_id (str): The ID of the workspace where the base will be created.

        Returns:
            dict: The response from the API containing details of the created base, or None if an error occurred.
        """
        default_table_structure = [{
            "name": "Table1",
            "fields": [
                {"name": "Field1", "type": "singleLineText"},
                {"name": "Field2", "type": "singleLineText"}
            ]
        }]
        data = {
            "name": base_name,
            "tables": default_table_structure,  # This structure needs to match the API requirements
            "workspaceId": workspace_id
        }
        response = self._make_api_request("POST", "meta/bases", data)
        if response and 'id' in response:
            return response
        else:
            error_info = response.json() if response else "No response"
            print(f"Failed to create the base: {error_info}")
            return None

    def list_existing_bases(self):
        """
        Retrieves a list of existing bases.

        Returns:
            list: A list of dictionaries containing details of each base, or an empty list if an error occurred.
        """
        response = self._make_api_request("GET", "meta/bases")
        if response and 'bases' in response:
            return response['bases']
        else:
            print("Failed to retrieve existing bases or unexpected response format.")
            return []

    def display_existing_bases(self, bases):
        """
        Displays the existing bases in a user-friendly format.

        Args:
            bases (list): A list of bases, each represented as a dictionary.

        This method prints each base's name and ID.
        """
        print("Your Authorized Bases:")
        print("")
        for idx, base in enumerate(bases, start=1):
            print(f"{idx}. {base['name']} (ID: {base['id']})")

    def select_existing_base(self, bases):
        """
        Allows the user to select an existing base from a list.

        Args:
            bases (list): A list of bases, each represented as a dictionary.

        Returns:
            str: The ID of the selected base, or None if the selection is invalid.
        """
        while True:
            try:
                print("")
                choice = int(input("Enter the numeric value of the base you would like to use: "))
                print("")
                if choice in range(1, len(bases) + 1):
                    return bases[choice - 1]["id"]
                else:
                    print("Invalid selection. Please enter a numeric value within the list range.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def list_tables_in_base(self, base_id):
        """
        Fetches and displays tables from the specified Airtable base.

        Args:
            base_id (str): The ID of the base to fetch tables from.

        Returns:
            list: A list of tables, each represented as a dictionary, or None if an error occurs.
        """
        endpoint = f"meta/bases/{base_id}/tables"
        response = self._make_api_request("GET", endpoint)
        if response and 'tables' in response:
            tables = response['tables']
            if tables:
                return [{"id": table["id"], "name": table["name"]} for table in tables]
            else:
                print("No tables found in this base.")
                return None
        else:
            print(f"Error fetching tables.")
            return None    

    def get_tables(self, base_id):
        """
        Fetches tables and their structure from a specified base.

        Args:
            base_id (str): The ID of the base from which to fetch tables.

        Returns:
            list: A list of tables with their structure, or None if an error occurs.
        """
        endpoint = f"meta/bases/{base_id}/tables"
        response = self._make_api_request("GET", endpoint)
        if response and 'tables' in response:
            return [{"id": table["id"], "name": table["name"], "fields": table.get("fields", [])} for table in response['tables']]
        else:
            print("Failed to fetch tables.")
            return None

    def get_records(self, base_id, table_name):
        """
        Fetches all records from a specified table.

        Args:
            base_id (str): The ID of the base containing the table.
            table_name (str): The name of the table from which to fetch records.

        Returns:
            list: A list of records from the table, or an empty list if no records are found or an error occurs.
        """
        records = []
        offset = None
        while True:
            endpoint = f"{base_id}/{quote(table_name)}"
            params = {"offset": offset} if offset else {}
            response = self._make_api_request("GET", endpoint, params=params)
            if response and 'records' in response:
                records.extend(response['records'])
                offset = response.get('offset')
                if not offset:
                    break
            else:
                print("Failed to fetch records.")
                break
        return records

    def create_table_with_structure(self, base_id, table_name, fields):
        """
        Creates a new table with the specified structure in a base.

        Args:
            base_id (str): The ID of the base where the new table will be created.
            table_name (str): The name of the new table to be created.
            fields (list): A list of field definitions for the new table.

        Returns:
            dict: The response from the API containing details of the created table, or None if an error occurred.
        """
        endpoint = f"meta/bases/{base_id}/tables"
        data = {
            "name": table_name,
            "fields": fields
        }
        response = self._make_api_request("POST", endpoint, data=data)
        if response and 'id' in response:
            print(f"Table '{table_name}' created with ID {response['id']}.")
            return response
        else:
            print(f"Failed to create table '{table_name}'.")
            return None

    def get_table_structure(self, base_id, table_name):
        """
        Fetches the structure of a specified table.

        Args:
            base_id (str): The ID of the base containing the table.
            table_name (str): The name of the table whose structure is to be fetched.

        Returns:
            dict: The structure of the table, or None if an error occurs.
        """
        # Implementation for fetching field definitions
        # ...

    def get_records_from_table(self, base_id, table_name):
        """
        Fetches all records from a specified table.

        Args:
            base_id (str): The ID of the base containing the table.
            table_name (str): The name of the table from which to fetch records.

        Returns:
            list: A list of records from the table, or an empty list if no records are found or an error occurs.
        """
        # Similar implementation to the get_records method
        # ...

    def insert_records_into_table(self, base_id, table_name, records):
        """
        Inserts records into a specified table.

        Args:
            base_id (str): The ID of the base containing the table.
            table_name (str): The name of the table where records will be inserted.
            records (list): A list of records to be inserted into the table.

        Returns:
            list: A list of responses from the API for each inserted record, or None if an error occurs.
        """
        # Implementation for inserting records
        # Handling batch insertion and rate limits if necessary
        # ...
