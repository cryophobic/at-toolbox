import requests

class Toolbox:

    def __init__(self, api_key):
        self.api_base = "https://api.airtable.com/v0"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_api_request(self, method, endpoint, data=None):
        url = f"{self.api_base}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            # Handle errors here, for example:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def create_base(self, base_name, workspace_id):
            """Creates a new base in the specified workspace."""
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
        response = self._make_api_request("GET", "meta/bases")
        if response and 'bases' in response:
            return response['bases']
        else:
            print("Failed to retrieve existing bases or unexpected response format.")
            return []

    def display_existing_bases(self, bases):
        print("Your Authorized Bases:")
        print("")
        for idx, base in enumerate(bases, start=1):
            print(f"{idx}. {base['name']} (ID: {base['id']})")

    def select_existing_base(self, bases):
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
        """ Fetches and displays tables from the specified Airtable base. """
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
        """ Fetches tables and their structure from a base """
        endpoint = f"meta/bases/{base_id}/tables"
        response = self._make_api_request("GET", endpoint)
        if response and 'tables' in response:
            return [{"id": table["id"], "name": table["name"], "fields": table.get("fields", [])} for table in response['tables']]
        else:
            print("Failed to fetch tables.")
            return None

    def get_records(self, base_id, table_name):
        """ Fetches all records from a table """
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

"""
This whole section is here to Duplicate Tables to Another Base
It could get messy.
"""      
def create_table_with_structure(self, base_id, table_name, fields):
    """Creates a new table with the specified structure."""
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
    """Fetches the structure of a table."""
    # API call to fetch field definitions
    # Return structure (field names and types)
    pass

def get_records_from_table(self, base_id, table_name):
    """Fetches all records from a table."""
    # API call to fetch all records
    # Handle pagination if necessary
    pass

def insert_records_into_table(self, base_id, table_name, records):
    """Inserts records into a table."""
    # API call to insert records
    # Handle batch insertion and rate limits if necessary
    pass