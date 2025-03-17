import json
from typing import Any

from src.utils.logger import logger


class ConfigService:
    """
    ConfigService provides a convinient way to read and edit
    configuration JSON files for Server and Client objects.
    """
    def __init__(self, path_to_config_file: str):
        """
        Initializes ConfigService.
        :param path_to_config_file: Path to the config.json
        """
        self.config_path = path_to_config_file
        self.config_data = self._load_config()

    def _load_config(self):
        """
        Loads soda
        """
        try:
            with open(self.config_path, 'r') as cfg:
                return json.load(cfg)
        except Exception as e:
            logger.error(f'Failed to open a config file: {e}')

    def _save_config(self):
        """
        Saves config file.
        """
        with open(self.config_path, 'w') as cfg:
            json.dump(self.config_data, cfg)

    def set_value(self, key: str, value: Any) -> None:
        """
        This method is used to change values in key:value pairs of config.JSON
        :param key: Specify key to change its value
        :param value: Specify new value
        """
        try:
            self.config_data[key] = value
            self._save_config()
        except Exception as e:
            logger.error(f'Failed to save changes to a config file: {e}')