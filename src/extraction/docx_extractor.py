"""
DOCX text extraction module
"""

from typing import Optional
import docx


class DOCXExtractor:
    """Extract text from DOCX files"""
    
    def extract(self, file_path: str) -> Optional[str]:
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            doc = docx.Document(file_path)
            
            # Extract text from all paragraphs
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            # Combine paragraphs
            full_text = '\n'.join(paragraphs)
            
            if not full_text.strip():
                # Empty document
                return None
            
            return full_text
            
        except Exception as e:
            print(f"Error extracting DOCX text: {str(e)}")
            return None
