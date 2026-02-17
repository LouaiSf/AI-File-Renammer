"""
Configuration loader for YAML config files
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Load and validate configuration"""
    
    @staticmethod
    def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Validate config
        ConfigLoader._validate_config(config)
        
        return config
    
    @staticmethod
    def _validate_config(config: Dict[str, Any]):
        """
        Validate configuration
        
        Args:
            config: Configuration dictionary
            
        Raises:
            ValueError: If configuration is invalid
        """
        # Check required sections
        required_sections = ['supported_extensions', 'classifier', 'filename_generator']
        
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required config section: {section}")
        
        # Validate classifier type
        valid_classifier_types = ['rule_based', 'ml', 'llm', 'transformer', 'zero_shot']
        classifier_type = config['classifier'].get('type')
        if classifier_type not in valid_classifier_types:
            raise ValueError(f"Invalid classifier type: {classifier_type}")
        
        # Validate generator type
        valid_generator_types = ['template', 'dynamic_template', 'llm', 'summarization']
        generator_type = config['filename_generator'].get('type')
        if generator_type not in valid_generator_types:
            raise ValueError(f"Invalid generator type: {generator_type}")
