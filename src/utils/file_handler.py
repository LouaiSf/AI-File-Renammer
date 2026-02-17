"""
File handling utilities (scanning, renaming, conflict resolution)
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict


class FileHandler:
    """Handle file operations (scanning, renaming, conflict resolution)"""
    
    def __init__(self, config: Dict = None):
        """Initialize file handler"""
        self.config = config or {}
        self.supported_extensions = self.config.get('supported_extensions', ['.pdf', '.txt', '.docx'])
        self.recursive = self.config.get('scan_options', {}).get('recursive', True)
        self.conflict_strategy = self.config.get('conflict_resolution', {}).get('strategy', 'version')
    
    def scan_folder(self, folder_path: str) -> List[str]:
        """
        Scan folder for supported files
        
        Args:
            folder_path: Path to folder to scan
            
        Returns:
            List of file paths
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        if not os.path.isdir(folder_path):
            raise ValueError(f"Not a directory: {folder_path}")
        
        files = []
        
        if self.recursive:
            # Recursive scan
            for root, _, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if self._is_supported_file(file_path):
                        files.append(file_path)
        else:
            # Non-recursive scan
            for item in os.listdir(folder_path):
                file_path = os.path.join(folder_path, item)
                if os.path.isfile(file_path) and self._is_supported_file(file_path):
                    files.append(file_path)
        
        return files
    
    def _is_supported_file(self, file_path: str) -> bool:
        """
        Check if file extension is supported
        
        Args:
            file_path: Path to file
            
        Returns:
            True if supported, False otherwise
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.supported_extensions
    
    def rename_file(self, original_path: str, new_filename: str) -> str:
        """
        Rename file safely (with conflict resolution)
        
        Args:
            original_path: Original file path
            new_filename: New filename (without extension)
            
        Returns:
            New file path
        """
        if not os.path.exists(original_path):
            raise FileNotFoundError(f"File not found: {original_path}")
        
        # Get directory and extension
        directory = os.path.dirname(original_path)
        _, ext = os.path.splitext(original_path)
        
        # Build new path
        new_path = os.path.join(directory, new_filename + ext)
        
        # Resolve conflicts
        new_path = self._resolve_conflict(new_path)
        
        # Rename file
        try:
            shutil.move(original_path, new_path)
            return new_path
        except Exception as e:
            raise Exception(f"Failed to rename file: {str(e)}")
    
    def _resolve_conflict(self, target_path: str) -> str:
        """
        Resolve filename conflicts
        
        Args:
            target_path: Desired file path
            
        Returns:
            Safe file path (non-conflicting)
        """
        if not os.path.exists(target_path):
            return target_path
        
        # Extract components
        directory = os.path.dirname(target_path)
        filename = os.path.basename(target_path)
        name, ext = os.path.splitext(filename)
        
        if self.conflict_strategy == 'version':
            # Add version number (file_v2.pdf, file_v3.pdf, etc.)
            counter = 2
            while True:
                new_name = f"{name}_v{counter}{ext}"
                new_path = os.path.join(directory, new_name)
                if not os.path.exists(new_path):
                    return new_path
                counter += 1
        
        elif self.conflict_strategy == 'timestamp':
            # Add timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_name = f"{name}_{timestamp}{ext}"
            return os.path.join(directory, new_name)
        
        elif self.conflict_strategy == 'hash':
            # Add hash of original filename
            import hashlib
            hash_suffix = hashlib.md5(name.encode()).hexdigest()[:8]
            new_name = f"{name}_{hash_suffix}{ext}"
            return os.path.join(directory, new_name)
        
        else:
            # Default to version strategy
            return self._resolve_conflict_version(target_path)
