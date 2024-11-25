"""
This module contains the logger service.
"""
import copy
import logging
import os
from logging.handlers import RotatingFileHandler


class ConsoleFormatter(logging.Formatter):
    """
    Formatter for console output - strips color codes
    """


class FileFormatter(logging.Formatter):
    """
    Formatter for file output - strips color codes
    """

    def format(self, record):
        alt_record = copy.copy(record)
        if hasattr(alt_record, 'msg'):
            if isinstance(alt_record.msg, str):
                alt_record.msg = alt_record.msg.replace('\033[92m', '').replace('\033[0m', '')
        return super().format(alt_record)


class LoggerService:
    """
    This class provides a logger service.
    """

    def __init__(self):
        self.logger = logging.getLogger('notes_be')
        self.setup_logger()

    def setup_logger(self):
        """
        Set up the logger with file and console handlers.
        """
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            ConsoleFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        os.makedirs('logs', exist_ok=True)

        # File handler with stripped colors
        file_formatter = FileFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        os.makedirs('logs', exist_ok=True)
        log_file = 'logs/notes_be.log'
        with open(log_file, 'a', encoding='utf-8'):
            pass
        file_handler = (
            RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5, encoding='utf-8'))
        file_handler.setFormatter(file_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
