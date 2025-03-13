from datetime import datetime

from src.enums.logger import LoggerLevel


class Logger:
    def debug(self, message: str) -> None:
        """
        Log message with level DEBUG
        """
        self._log(message, LoggerLevel.debug)

    def info(self, message: str) -> None:
        """
        Log message with level INFO
        """
        self._log(message, LoggerLevel.info)

    def warning(self, message: str) -> None:
        """
        Log message with level WARNING
        """
        self._log(message, LoggerLevel.warning)

    def error(self, message: str) -> None:
        """
        Log message with level ERROR
        """

        self._log(message, LoggerLevel.error)

    @staticmethod
    def _log(message: str, level: LoggerLevel) -> None:
        """
        Log message with given log level
        """
        timestamp = datetime.now().replace(microsecond=0)
        print(f"[{level.value}][{timestamp}] {message.capitalize()}")


logger = Logger()
