"""
Template-based filename generator (reference implementation)
"""

import re
from typing import Dict
from datetime import datetime
from .base import FilenameGenerator


class TemplateFilenameGenerator(FilenameGenerator):
    """
    Template-based filename generator
    
    Uses configurable templates per document type.
    This is the reference implementation and can be replaced with
    AI-generated names, semantic summarization, etc.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize generator with templates"""
        self.config = config or {}
        self.templates = self._load_templates()
        self.max_length = self.config.get('filename_generator', {}).get('max_length', 150)
    
    def _load_templates(self) -> Dict[str, str]:
        """Load templates from config"""
        return self.config.get('filename_generator', {}).get('templates', {
            'Invoice': '{vendor}_Invoice_{invoice_number}_{date}',
            'Contract': 'Contract_{parties}_{date}',
            'ID': '{doc_type}_{person_name}_{issue_date}',
            'BankStatement': '{bank}_Statement_{year}-{month}',
            'Receipt': 'Receipt_{vendor}_{amount}_{date}',
            'Unknown': 'Unknown_{date}',
            'default': '{doc_type}_{primary_entity}_{date}'
        })
    
    def generate(self, metadata: Dict[str, any], classification: Dict[str, any], 
                 original_filename: str) -> str:
        """
        Generate filename using templates
        
        Args:
            metadata: Extracted metadata
            classification: Classification result
            original_filename: Original filename
            
        Returns:
            Generated filename (sanitized, without extension)
        """
        doc_type = classification.get('document_type', 'Unknown')
        
        # Get template for document type
        template = self.templates.get(doc_type, self.templates.get('default'))
        
        # Try to fill template
        try:
            filename = self._fill_template(template, metadata, classification)
        except Exception as e:
            # Fallback if template filling fails
            filename = self._generate_fallback(metadata, classification, original_filename)
        
        # Sanitize filename
        filename = self._sanitize_filename(filename)
        
        # Enforce length constraint
        filename = self._enforce_length(filename)
        
        return filename
    
    def _fill_template(self, template: str, metadata: Dict, classification: Dict) -> str:
        """
        Fill template with metadata
        
        Args:
            template: Template string
            metadata: Metadata dictionary
            classification: Classification dictionary
            
        Returns:
            Filled template
        """
        # Prepare variables for template
        variables = {
            'doc_type': classification.get('document_type', 'Unknown'),
            'vendor': metadata.get('organization_name', ''),
            'parties': metadata.get('organization_name', ''),
            'person_name': metadata.get('person_name', ''),
            'primary_entity': metadata.get('organization_name') or metadata.get('person_name', ''),
            'date': metadata.get('date', ''),
            'issue_date': metadata.get('date', ''),
            'invoice_number': metadata.get('invoice_number', ''),
            'amount': metadata.get('amount', ''),
            'bank': metadata.get('organization_name', ''),
            'year': metadata.get('year', ''),
            'month': metadata.get('month', ''),
        }
        
        # Check if all required variables are present
        required_vars = re.findall(r'\{(\w+)\}', template)
        missing_vars = [var for var in required_vars if not variables.get(var)]
        
        if missing_vars:
            # Use fallback logic for missing variables
            return self._apply_fallback_logic(metadata, classification)
        
        # Fill template
        try:
            filename = template.format(**variables)
            return filename
        except KeyError:
            return self._apply_fallback_logic(metadata, classification)
    
    def _apply_fallback_logic(self, metadata: Dict, classification: Dict) -> str:
        """
        Apply fallback logic when template cannot be filled
        
        Args:
            metadata: Metadata dictionary
            classification: Classification dictionary
            
        Returns:
            Fallback filename
        """
        doc_type = classification.get('document_type', 'Unknown')
        date = metadata.get('date')
        entity = metadata.get('organization_name') or metadata.get('person_name')
        
        # Build filename based on available data
        parts = [doc_type]
        
        if entity:
            parts.append(entity)
        
        if date:
            parts.append(date)
        elif metadata.get('file_modified_date'):
            parts.append(metadata['file_modified_date'])
        else:
            # Use timestamp as last resort
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            parts.append(timestamp)
        
        if not entity and not date:
            parts.append('NoMetadata')
        
        return '_'.join(parts)
    
    def _generate_fallback(self, metadata: Dict, classification: Dict, 
                          original_filename: str) -> str:
        """
        Generate fallback filename when all else fails
        
        Args:
            metadata: Metadata dictionary
            classification: Classification dictionary
            original_filename: Original filename
            
        Returns:
            Fallback filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = original_filename.rsplit('.', 1)[0]  # Remove extension
        return f"{base_name}_{timestamp}"
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename (remove invalid characters)
        
        Args:
            filename: Raw filename
            
        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        invalid_chars = r'[<>:"/\\|?*]'
        filename = re.sub(invalid_chars, '', filename)
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove multiple underscores
        filename = re.sub(r'_+', '_', filename)
        
        # Remove leading/trailing underscores and dots
        filename = filename.strip('_.')
        
        return filename
    
    def _enforce_length(self, filename: str) -> str:
        """
        Enforce maximum filename length
        
        Args:
            filename: Filename to check
            
        Returns:
            Filename truncated if necessary
        """
        if len(filename) <= self.max_length:
            return filename
        
        # Truncate from middle and add ellipsis
        half = (self.max_length - 3) // 2
        return filename[:half] + '...' + filename[-half:]
