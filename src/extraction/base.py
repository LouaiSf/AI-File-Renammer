"""
Base text extractor with unified interface for all file types
"""

import os
from typing import Optional


class TextExtractor:
    """
    Unified text extraction interface
    Routes extraction to appropriate handler based on file extension
    """
    
    def __init__(self):
        """Initialize extractors for supported file types"""
        from .pdf_extractor import PDFExtractor
        from .txt_extractor import TXTExtractor
        from .docx_extractor import DOCXExtractor
        
        self.extractors = {
            '.pdf': PDFExtractor(),
            '.txt': TXTExtractor(),
            '.docx': DOCXExtractor()
        }
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extract text from file based on extension
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text or None if extraction fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Get appropriate extractor
        extractor = self.extractors.get(ext)
        if not extractor:
            raise ValueError(f"Unsupported file extension: {ext}")
        
        # Extract text
        try:
            return extractor.extract(file_path)
        except Exception as e:
            raise Exception(f"Failed to extract text from {file_path}: {str(e)}")
