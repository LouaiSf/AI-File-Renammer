"""
PDF text extraction module
"""

from typing import Optional
import pypdf


class PDFExtractor:
    """Extract text from PDF files (text-based only)"""
    
    def extract(self, file_path: str) -> Optional[str]:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text or None if PDF is not text-based
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                # Check if PDF has text
                if len(pdf_reader.pages) == 0:
                    return None
                
                # Extract text from all pages
                text_parts = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                
                # Combine all text
                full_text = '\n'.join(text_parts)
                
                # Check if meaningful text was extracted
                if len(full_text.strip()) < 10:
                    # Likely a scanned PDF or image-only
                    return None
                
                return full_text
                
        except Exception as e:
            # Log error and return None
            print(f"Error extracting PDF text: {str(e)}")
            return None
