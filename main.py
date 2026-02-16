"""
AI File Renamer - Main Entry Point
Offline text-based document renaming system
"""

import argparse
import sys
from pathlib import Path

from src.core.pipeline import FileRenamingPipeline
from src.utils.logger import Logger


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description='AI File Renamer - Automatically rename documents based on content'
    )
    
    parser.add_argument(
        'folder_path',
        type=str,
        help='Path to folder containing files to rename'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview rename results without actually renaming files'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output (DEBUG level logging)'
    )
    
    parser.add_argument(
        '--non-recursive',
        action='store_true',
        help='Do not scan subdirectories'
    )
    
    args = parser.parse_args()
    
    # Validate folder path
    folder_path = Path(args.folder_path)
    if not folder_path.exists():
        print(f"Error: Folder not found: {args.folder_path}")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"Error: Not a directory: {args.folder_path}")
        sys.exit(1)
    
    # Validate config file
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)
    
    try:
        # Initialize pipeline
        print(f"Initializing AI File Renamer...")
        print(f"Config: {args.config}")
        print(f"Target folder: {args.folder_path}")
        print()
        
        pipeline = FileRenamingPipeline(config_path=args.config)
        
        # Process files
        if args.preview:
            print("=== PREVIEW MODE (no files will be renamed) ===")
            # TODO: Implement preview mode
            print("Preview mode not yet implemented")
        else:
            print("=== PROCESSING FILES ===")
            stats = pipeline.process_folder(str(folder_path))
            
            # Print summary
            print()
            print("=== PROCESSING COMPLETE ===")
            print(f"Total files: {stats['total']}")
            print(f"Successfully renamed: {stats['success']}")
            print(f"Failed: {stats['failed']}")
            print(f"Skipped: {stats['skipped']}")
            print()
            print(f"Check log file for details: logs/file_renamer.log")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
