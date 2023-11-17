# debug_helper.py

import json
import requests

class DebugHelper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def pretty_print_json(self, data):
        print(json.dumps(data, indent=4, sort_keys=True))

    def log_request(self, method, url, headers=None, data=None):
        print(f"Request Method: {method}")
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        if data:
            print(f"Request Body: {json.dumps(data, indent=4)}")

    def log_response(self, response):
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.text}")

    def make_debug_api_request(self, method, url, data=None):
        self.log_request(method, url, self.headers, data)
        response = requests.request(method, url, headers=self.headers, json=data)
        self.log_response(response)
        return response

    # ... Add any other debugging methods you find useful
