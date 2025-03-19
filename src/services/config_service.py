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

    def _load_config(self) -> dict | None:
        """
        Loads govno
        """
        try:
            with open(self.config_path, 'r', encoding="UTF-8") as cfg:
                return json.load(cfg)
        except Exception as e:
            logger.error(f'Failed to open a config file: {e}')

    def _save_config(self):
        """
        Saves config file.
        """
        with open(self.config_path, 'w', encoding='UTF-8') as cfg:
            json.dump(self.config_data, cfg, indent=4)

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

    def get_value(self, key: str) -> Any:
        """
        Returns value of specified key. If an error occurs,
        returns logger.error instead.
        :param key: Specify key to get its value.
        """
        if key in self.config_data:
            return self.config_data[key]
        else:
            return logger.error(f'Failed to get value of {key}: could not find {key} in cfg')
