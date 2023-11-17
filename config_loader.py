import yaml

def load_config(config_path='config.yaml'):
    """
    Loads configuration settings from a YAML file.

    This function reads the specified YAML file and loads its contents as a Python dictionary. 
    It's primarily used to load configuration settings for the application.

    Args:
        config_path (str): The path to the configuration file. Defaults to 'config.yaml'.

    Returns:
        dict: A dictionary containing the configuration settings.
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing the configuration file: {e}")
        return None