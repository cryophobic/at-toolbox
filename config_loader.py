import yaml

def load_config(config_path='config.yaml'):
    """
    Loads configuration settings from a YAML file.

    Args:
    config_path (str): The path to the configuration file.

    Returns:
    dict: A dictionary containing the configuration settings.
    """
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            return config
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None