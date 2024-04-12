import os
import toml


def load_secrets_from_toml(toml_file_path):
    """
    Loads secrets from a .toml file and sets them as environment variables.

    Args:
        toml_file_path (str): The path to the .toml file.

    Returns:
        None
    """
    # Load the secrets from the .toml file
    secrets = toml.load(toml_file_path)

    # Set the secrets as environment variables
    for section, values in secrets.items():
        for key, value in values.items():
            os.environ[f"{section.upper()}_{key.upper()}"] = str(value)

