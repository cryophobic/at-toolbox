import json
import requests

class DebugHelper:
    """
    Provides debugging tools for API interactions.

    This class assists in debugging by offering methods for logging and handling API request responses.

    Attributes:
        api_key (str): The API key used for authenticating with the Airtable API.
        headers (dict): Headers to be used in API requests.
    """

    def __init__(self, api_key):
        """
        Initializes the DebugHelper with the given API key.

        Args:
            api_key (str): The API key used for authenticating with the Airtable API.
        """
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
        }

    def log_response(self, response):
        """
        Logs the response from an API request.

        This method is used for logging the details of API responses, particularly useful for debugging.

        Args:
            response (requests.Response): The response object from an API request.
        """
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

    def handle_api_error(self, response):
        """
        Handles errors from API requests.

        This method provides a structured way to handle and log errors that occur during API requests.

        Args:
            response (requests.Response): The response object from an API request.
        """
        # Implementation for error handling
        # ...
