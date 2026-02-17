"""
Base filename generator interface - all generators must implement this
"""

from abc import ABC, abstractmethod
from typing import Dict


class FilenameGenerator(ABC):
    """
    Abstract base class for filename generators
    
    All generator implementations must follow this interface contract
    to ensure they are swappable without modifying other modules
    """
    
    @abstractmethod
    def generate(self, metadata: Dict[str, any], classification: Dict[str, any], 
                 original_filename: str) -> str:
        """
        Generate filename from metadata and classification
        
        Args:
            metadata: Extracted metadata (dates, entities, keywords)
            classification: Classification result (type, confidence)
            original_filename: Original file name (for fallback)
            
        Returns:
            Sanitized filename (without extension)
            
        Example:
            "Invoice_AcmeCorp_2026-02-15"
        """
        pass
