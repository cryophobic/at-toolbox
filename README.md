# Airtable Toolbox

## Description
This handy set of tools is designed to interact with the Airtable API, providing functionalities such as creating bases, managing tables, and handling records. It's built in Python and offers a user-friendly command-line interface.

## Features
- Create new bases in Airtable.
- List and select from existing bases.
- Manage tables within the selected base.
- Duplicate tables to other bases.
- User-friendly command-line interactions.

## How to Use
1. Ensure you have Python installed on your system.
2. Clone or download this repository.
3. Install required packages: `pip install -r requirements.txt`.
4. Run the utility: `python main.py`.

## Initial Setup
Before running the utility, you need to set up the `config.yaml` file. This file contains necessary configuration settings like the Airtable API key and workspace details.

### Configuring `config.yaml`
1. Create a file named `config.yaml` in the project directory.
2. Add your Airtable API key and other configurations. Here's an example structure:

    ```yaml
    api_key: YOUR_AIRTABLE_API_KEY
    workspaces:
      - id: WORKSPACE_ID_1
        name: Workspace 1
      - id: WORKSPACE_ID_2
        name: Workspace 2
    ```

    Replace `YOUR_AIRTABLE_API_KEY` with your actual Airtable API key, and `WORKSPACE_ID_1`, `WORKSPACE_ID_2`, etc., with your actual workspace IDs and names.

## Configuration
The tool relies on the `config.yaml` file for API keys and other configurations. Ensure this file is correctly set up before running the tool.

## Documentation
Each Python file in this project is well-documented with detailed docstrings explaining the functionalities, parameters, and return values of classes and functions.
