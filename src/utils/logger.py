"""
Logging module for tracking all operations
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class Logger:
    """
    Logger for file renaming operations
    Supports JSON and text log formats
    """
    
    def __init__(self, config: Dict = None):
        """Initialize logger with configuration"""
        self.config = config or {}
        logging_config = self.config.get('logging', {})
        
        self.log_level = logging_config.get('level', 'INFO')
        self.log_format = logging_config.get('format', 'json')
        self.log_file = logging_config.get('log_file', 'logs/file_renamer.log')
        self.console_output = logging_config.get('console_output', True)
        
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup Python logging"""
        # Ensure log directory exists
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('file_renamer')
        self.logger.setLevel(getattr(logging, self.log_level))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, self.log_level))
        
        # Console handler (if enabled)
        if self.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, self.log_level))
            
            # Formatter
            if self.log_format == 'json':
                formatter = logging.Formatter('%(message)s')
            else:
                formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(file_handler)
    
    def _format_log(self, level: str, message: str, **kwargs) -> str:
        """
        Format log entry
        
        Args:
            level: Log level
            message: Log message
            **kwargs: Additional fields
            
        Returns:
            Formatted log entry
        """
        if self.log_format == 'json':
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'level': level,
                'message': message,
                **kwargs
            }
            return json.dumps(log_entry, ensure_ascii=False)
        else:
            return message
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        log_msg = self._format_log('DEBUG', message, **kwargs)
        self.logger.debug(log_msg)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        log_msg = self._format_log('INFO', message, **kwargs)
        self.logger.info(log_msg)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        log_msg = self._format_log('WARNING', message, **kwargs)
        self.logger.warning(log_msg)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        log_msg = self._format_log('ERROR', message, **kwargs)
        self.logger.error(log_msg)
