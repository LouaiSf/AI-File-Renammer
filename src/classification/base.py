"""
Base classifier interface - all classifiers must implement this
"""

from abc import ABC, abstractmethod
from typing import Dict


class DocumentClassifier(ABC):
    """
    Abstract base class for document classifiers
    
    All classifier implementations must follow this interface contract
    to ensure they are swappable without modifying other modules
    """
    
    @abstractmethod
    def classify(self, text: str) -> Dict[str, any]:
        """
        Classify document based on text content
        
        Args:
            text: Cleaned document text
            
        Returns:
            Dictionary with:
                - document_type: str (e.g., "Invoice", "Contract", "ID", etc.)
                - confidence: float (0.0 to 1.0)
                
        Example:
            {
                "document_type": "Invoice",
                "confidence": 0.85
            }
        """
        pass
