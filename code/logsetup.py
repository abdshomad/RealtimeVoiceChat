import logging
import time
import os
from datetime import datetime
from colors import Colors # Assuming 'colors' library is installed (pip install ansicolors) or your custom Colors class
from typing import Optional # Added for type hint consistency if needed elsewhere, though not strictly used in current args/returns

# --- Define Custom Formatter to handle time locally ---
class CustomTimeFormatter(logging.Formatter):
    """
    A logging Formatter that displays timestamps as MM:SS.cs using local time.

    Inherits from `logging.Formatter` and overrides the `formatTime` method
    to provide a specific, concise timestamp format suitable for console output,
    using the local time zone derived from the log record's creation time.
    """

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """
        Formats the log record's creation time into MM:SS.cs format.

        Uses `time.localtime` to convert the record's creation timestamp and
        formats it as minutes, seconds, and centiseconds. The `datefmt` argument
        provided by the base class is ignored in this custom implementation.

        Args:
            record: The log record whose creation time needs formatting.
            datefmt: An optional date format string (ignored by this method).

        Returns:
            A string representing the formatted time (e.g., "59:23.18").
        """
        # Use localtime as originally intended, but locally within this formatter
        now = time.localtime(record.created)
        cs = int((record.created % 1) * 100)  # centiseconds
        # Format the time string as required
        s = time.strftime("%M:%S", now) + f".{cs:02d}"
        return s

class FileTimeFormatter(logging.Formatter):
    """
    A logging Formatter for file output with full timestamps.
    """
    
    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """
        Formats the log record's creation time into full datetime format.
        """
        now = time.localtime(record.created)
        return time.strftime("%Y-%m-%d %H:%M:%S", now)

def setup_logging(level: int = logging.INFO, enable_file_logging: bool = True, 
                  file_level: int = logging.DEBUG, console_level: int = logging.INFO) -> None:
    """
    Configures the root logger for console and file output with custom formats and levels.

    Sets up a `StreamHandler` for console output and a `FileHandler` for file output
    if file logging is enabled. Applies custom formatters for both handlers.
    Creates logs directory if it doesn't exist and generates timestamped log files.
    Allows different log levels for console and file output.

    Args:
        level: The minimum logging level for the root logger
               (e.g., `logging.DEBUG`, `logging.INFO`). Defaults to `logging.INFO`.
        enable_file_logging: Whether to enable file logging. Defaults to True.
        file_level: The minimum logging level for file output. Defaults to `logging.DEBUG`.
        console_level: The minimum logging level for console output. Defaults to `logging.INFO`.
    """
    # Check if the root logger already has handlers to avoid adding them multiple times
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():
        # Set the level on the logger itself
        root_logger.setLevel(min(level, file_level, console_level))

        # --- Console Handler Setup ---
        # Define Format String for console
        prefix = Colors.apply("🖥️").gray
        timestamp = Colors.apply("%(asctime)s").blue
        levelname = Colors.apply("%(levelname)-4.4s").green.bold
        message = Colors.apply("%(message)s")
        logger_name = Colors.apply("%(name)-10.10s").gray

        console_format = f"{timestamp} {logger_name} {levelname} {message}"
        
        # Create console formatter and handler
        console_formatter = CustomTimeFormatter(console_format)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(console_level)
        root_logger.addHandler(console_handler)

        # --- File Handler Setup ---
        if enable_file_logging:
            try:
                # Ensure logs directory exists
                logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
                os.makedirs(logs_dir, exist_ok=True)
                
                # Generate timestamped log filename
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_filename = f"server_{timestamp_str}.log"
                log_filepath = os.path.join(logs_dir, log_filename)
                
                # Define format string for file (without colors, with more detail)
                file_format = "%(asctime)s %(name)-15.15s %(levelname)-8.8s %(filename)s:%(lineno)d - %(message)s"
                
                # Create file formatter and handler
                file_formatter = FileTimeFormatter(file_format)
                file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
                file_handler.setFormatter(file_formatter)
                file_handler.setLevel(file_level)
                root_logger.addHandler(file_handler)
                
                # Log the file logging setup
                root_logger.info(f"📁 File logging enabled: {log_filepath}")
                root_logger.debug(f"📁 File log level: {logging.getLevelName(file_level)}")
                root_logger.debug(f"🖥️ Console log level: {logging.getLevelName(console_level)}")
                
            except Exception as e:
                # If file logging fails, log the error to console only
                root_logger.warning(f"⚠️ Failed to setup file logging: {e}")
                root_logger.warning("⚠️ Continuing with console logging only")

def get_log_file_path() -> str:
    """
    Returns the path to the current log file.
    
    Returns:
        The path to the current log file, or empty string if file logging is not enabled.
    """
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler.baseFilename
    return ""

def get_log_stats() -> dict:
    """
    Returns statistics about the current logging setup.
    
    Returns:
        A dictionary with logging statistics including file path, log levels, etc.
    """
    root_logger = logging.getLogger()
    stats = {
        "file_path": get_log_file_path(),
        "handlers_count": len(root_logger.handlers),
        "logger_level": logging.getLevelName(root_logger.level),
        "handlers": []
    }
    
    for i, handler in enumerate(root_logger.handlers):
        handler_info = {
            "index": i,
            "type": type(handler).__name__,
            "level": logging.getLevelName(handler.level)
        }
        if isinstance(handler, logging.FileHandler):
            handler_info["file_path"] = handler.baseFilename
        stats["handlers"].append(handler_info)
    
    return stats
