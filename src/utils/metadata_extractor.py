"""
Metadata extraction from text (dates, entities, keywords)
"""

import re
import os
from typing import Dict, List, Optional
from datetime import datetime
from dateutil import parser


class MetadataExtractor:
    """Extract metadata from document text"""
    
    def __init__(self, config: Dict = None):
        """Initialize metadata extractor"""
        self.config = config or {}
        self.date_format = self.config.get('date_format', {}).get('output', '%Y-%m-%d')
        self.max_keywords = self.config.get('metadata', {}).get('max_keywords', 3)
        self.use_file_date_fallback = self.config.get('metadata', {}).get('use_file_date_fallback', True)
    
    def extract(self, text: str, file_path: str = None) -> Dict[str, any]:
        """
        Extract all metadata from text
        
        Args:
            text: Cleaned document text
            file_path: Original file path (for fallback metadata)
            
        Returns:
            Dictionary with extracted metadata
        """
        metadata = {}
        
        # Extract dates
        dates = self.extract_dates(text)
        if dates:
            metadata['date'] = dates[0]  # Use first date found
        elif self.use_file_date_fallback and file_path:
            # Use file modified date as fallback
            modified_time = os.path.getmtime(file_path)
            metadata['date'] = datetime.fromtimestamp(modified_time).strftime(self.date_format)
            metadata['file_modified_date'] = metadata['date']
        
        # Extract entities
        entities = self.extract_entities(text)
        metadata.update(entities)
        
        # Extract keywords
        keywords = self.extract_keywords(text)
        if keywords:
            metadata['keywords'] = keywords
        
        return metadata
    
    def extract_dates(self, text: str) -> List[str]:
        """
        Extract dates from text
        
        Args:
            text: Document text
            
        Returns:
            List of dates in standardized format (YYYY-MM-DD)
        """
        dates = []
        
        # Common date patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # DD/MM/YYYY or MM/DD/YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY-MM-DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',    # DD Month YYYY
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group()
                try:
                    # Parse date using dateutil
                    parsed_date = parser.parse(date_str, fuzzy=False)
                    formatted_date = parsed_date.strftime(self.date_format)
                    if formatted_date not in dates:
                        dates.append(formatted_date)
                except (ValueError, parser.ParserError):
                    # Skip invalid dates
                    continue
        
        return dates
    
    def extract_entities(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract entities (organizations, persons) from text
        
        Args:
            text: Document text
            
        Returns:
            Dictionary with entity information
        """
        entities = {
            'organization_name': None,
            'person_name': None
        }
        
        # Simple pattern-based entity extraction
        # This can be improved with NER models
        
        # Look for organization indicators
        org_patterns = [
            r'(?:Company|Corporation|Corp|Inc|Ltd|LLC|Organization)[\s:]+([A-Z][A-Za-z\s&]+?)(?:\n|\.|\,)',
            r'([A-Z][A-Za-z\s&]+?)\s+(?:Company|Corporation|Corp|Inc|Ltd|LLC)',
        ]
        
        for pattern in org_patterns:
            match = re.search(pattern, text)
            if match:
                entities['organization_name'] = match.group(1).strip()
                break
        
        # Look for person name patterns
        person_patterns = [
            r'(?:Name|Employee|Client|Customer)[\s:]+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'\bMr\.|Ms\.|Mrs\.|Dr\.\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        ]
        
        for pattern in person_patterns:
            match = re.search(pattern, text)
            if match:
                entities['person_name'] = match.group(1).strip()
                break
        
        return entities
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Document text
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction based on frequency
        # This can be improved with TF-IDF or other methods
        
        # Remove common words
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Extract words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Count frequencies
        word_freq = {}
        for word in words:
            if word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords
        keywords = [word for word, _ in sorted_words[:self.max_keywords]]
        
        return keywords
