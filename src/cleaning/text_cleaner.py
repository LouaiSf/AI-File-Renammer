"""
Text cleaning and normalization
"""

import re


class TextCleaner:
    """Clean and normalize extracted text"""
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove non-printable characters
        text = self._remove_non_printable(text)
        
        # Normalize whitespace
        text = self._normalize_whitespace(text)
        
        # Normalize line breaks
        text = self._normalize_line_breaks(text)
        
        # Trim leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _remove_non_printable(self, text: str) -> str:
        """
        Remove non-printable characters
        
        Args:
            text: Input text
            
        Returns:
            Text with non-printable characters removed
        """
        # Keep printable characters, spaces, tabs, and newlines
        return ''.join(char for char in text if char.isprintable() or char in '\n\t ')
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace (remove extra spaces)
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace tabs with spaces
        text = text.replace('\t', ' ')
        
        return text
    
    def _normalize_line_breaks(self, text: str) -> str:
        """
        Normalize line breaks
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized line breaks
        """
        # Replace Windows line breaks with Unix style
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        
        # Replace multiple newlines with maximum 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text
