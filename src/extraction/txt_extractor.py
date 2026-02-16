"""
TXT text extraction module
"""

from typing import Optional


class TXTExtractor:
    """Extract text from TXT files"""
    
    def extract(self, file_path: str) -> Optional[str]:
        """
        Extract text from TXT file
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Extracted text or None if reading fails
        """
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    text = file.read()
                    
                    # Successfully read the file
                    if text:
                        return text
                    else:
                        return None
                        
            except UnicodeDecodeError:
                # Try next encoding
                continue
            except Exception as e:
                print(f"Error reading TXT file: {str(e)}")
                return None
        
        # All encodings failed
        print(f"Could not decode file with any supported encoding: {file_path}")
        return None
