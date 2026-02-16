"""
Main pipeline orchestration for file renaming process
"""

import os
from typing import List, Dict, Tuple
from pathlib import Path

from ..extraction.base import TextExtractor
from ..cleaning.text_cleaner import TextCleaner
from ..classification.base import DocumentClassifier
from ..naming.base import FilenameGenerator
from ..utils.logger import Logger
from ..utils.file_handler import FileHandler
from ..utils.config_loader import ConfigLoader


class FileRenamingPipeline:
    """
    Orchestrates the complete file renaming pipeline
    
    Pipeline stages:
    1. File Detection
    2. Text Extraction
    3. Text Cleaning
    4. Metadata Extraction
    5. Document Classification (swappable)
    6. Filename Generation (swappable)
    7. Safe Rename
    8. Logging
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize pipeline with configuration"""
        self.config = ConfigLoader.load_config(config_path)
        self.logger = Logger(self.config)
        self.file_handler = FileHandler(self.config)
        self.text_cleaner = TextCleaner()
        
        # Initialize swappable components based on config
        self.extractor = self._initialize_extractor()
        self.classifier = self._initialize_classifier()
        self.filename_generator = self._initialize_generator()
        
    def _initialize_extractor(self) -> TextExtractor:
        """Initialize text extractor"""
        from ..extraction.pdf_extractor import PDFExtractor
        from ..extraction.txt_extractor import TXTExtractor
        from ..extraction.docx_extractor import DOCXExtractor
        
        # Return a composite extractor that handles all types
        return TextExtractor()
    
    def _initialize_classifier(self) -> DocumentClassifier:
        """Initialize classifier based on config"""
        classifier_type = self.config.get('classifier', {}).get('type', 'rule_based')
        
        if classifier_type == 'rule_based':
            from ..classification.rule_based_classifier import RuleBasedClassifier
            return RuleBasedClassifier(self.config)
        # Add more classifier types here as they are implemented
        else:
            raise ValueError(f"Unknown classifier type: {classifier_type}")
    
    def _initialize_generator(self) -> FilenameGenerator:
        """Initialize filename generator based on config"""
        generator_type = self.config.get('filename_generator', {}).get('type', 'template')
        
        if generator_type == 'template':
            from ..naming.template_generator import TemplateFilenameGenerator
            return TemplateFilenameGenerator(self.config)
        # Add more generator types here as they are implemented
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")
    
    def process_folder(self, folder_path: str) -> Dict[str, any]:
        """
        Process all supported files in a folder
        
        Args:
            folder_path: Path to folder containing files to rename
            
        Returns:
            Dictionary with processing statistics
        """
        self.logger.info(f"Starting batch processing for folder: {folder_path}")
        
        # Scan for supported files
        files = self.file_handler.scan_folder(folder_path)
        self.logger.info(f"Found {len(files)} supported files")
        
        stats = {
            'total': len(files),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        # Process each file
        for file_path in files:
            try:
                result = self.process_file(file_path)
                if result['status'] == 'success':
                    stats['success'] += 1
                elif result['status'] == 'skipped':
                    stats['skipped'] += 1
                else:
                    stats['failed'] += 1
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {str(e)}")
                stats['failed'] += 1
        
        self.logger.info(f"Batch processing complete. Success: {stats['success']}, "
                        f"Failed: {stats['failed']}, Skipped: {stats['skipped']}")
        
        return stats
    
    def process_file(self, file_path: str) -> Dict[str, any]:
        """
        Process a single file through the complete pipeline
        
        Args:
            file_path: Path to file to process
            
        Returns:
            Dictionary with processing results
        """
        self.logger.debug(f"Processing file: {file_path}")
        
        original_filename = os.path.basename(file_path)
        
        try:
            # 1. Extract text
            raw_text = self.extractor.extract_text(file_path)
            if not raw_text:
                self.logger.warning(f"No text extracted from {original_filename}")
                return {'status': 'skipped', 'reason': 'empty_text'}
            
            # 2. Clean text
            cleaned_text = self.text_cleaner.clean_text(raw_text)
            
            # 3. Extract metadata
            metadata = self._extract_metadata(cleaned_text, file_path)
            
            # 4. Classify document
            classification = self.classifier.classify(cleaned_text)
            
            # 5. Generate filename
            new_filename = self.filename_generator.generate(
                metadata, 
                classification, 
                original_filename
            )
            
            # 6. Rename file safely
            new_path = self.file_handler.rename_file(file_path, new_filename)
            
            # 7. Log result
            result = {
                'status': 'success',
                'original': original_filename,
                'new': os.path.basename(new_path),
                'classification': classification,
                'metadata': metadata
            }
            
            self.logger.info(f"Successfully renamed: {original_filename} -> {os.path.basename(new_path)}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to process {original_filename}: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def _extract_metadata(self, text: str, file_path: str) -> Dict[str, any]:
        """
        Extract metadata from text
        
        Args:
            text: Cleaned text content
            file_path: Original file path (for fallback metadata)
            
        Returns:
            Dictionary with extracted metadata
        """
        from ..utils.metadata_extractor import MetadataExtractor
        
        extractor = MetadataExtractor(self.config)
        metadata = extractor.extract(text, file_path)
        
        return metadata
