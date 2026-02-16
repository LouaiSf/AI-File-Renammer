# AI File Renamer

An offline, modular document renaming system that automatically generates descriptive filenames based on document content.

## Features

- **Fully Offline**: No internet connection required
- **Modular Design**: Swappable classification and naming modules
- **Safe Renaming**: Automatic conflict resolution
- **Comprehensive Logging**: Track all operations
- **Multiple File Types**: Support for PDF, TXT, and DOCX

## Supported File Types

- `.pdf` (text-based PDFs only)
- `.txt` (UTF-8 and common encodings)
- `.docx` (Microsoft Word documents)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the system (optional):
Edit `config.yaml` to customize:
- Classifier type (rule-based, ML, LLM)
- Filename templates
- Logging preferences
- File scanning options

## Usage

### Basic Usage

Rename all supported files in a folder:

```bash
python main.py /path/to/folder
```

### Advanced Options

Preview rename results without changing files:
```bash
python main.py /path/to/folder --preview
```

Enable verbose output:
```bash
python main.py /path/to/folder --verbose
```

Scan only the target folder (not subdirectories):
```bash
python main.py /path/to/folder --non-recursive
```

Use custom configuration:
```bash
python main.py /path/to/folder --config custom_config.yaml
```

## Configuration

The system is configured via `config.yaml`. Key settings:

### Classifier Configuration

Choose classification method:
- `rule_based`: Keyword matching (default, no dependencies)
- `ml`: Machine learning classifier (requires training data)
- `llm`: Local LLM (requires model download)
- `zero_shot`: Transformer-based (requires transformers library)

### Filename Templates

Customize templates per document type:

```yaml
templates:
  Invoice: "{vendor}_Invoice_{invoice_number}_{date}"
  Contract: "Contract_{parties}_{date}"
  default: "{doc_type}_{primary_entity}_{date}"
```

### Logging

Configure log level, format, and destination:

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  format: "json"  # json or text
  log_file: "logs/file_renamer.log"
```

## Project Structure

```
ai-file-renamer/
├ src/
│   ├ core/              # Pipeline orchestration
│   ├ extraction/        # Text extraction (PDF, TXT, DOCX)
│   ├ cleaning/          # Text normalization
│   ├ classification/    # Document classification (SWAPPABLE)
│   ├ naming/            # Filename generation (SWAPPABLE)
│   └ utils/             # Logging, config, file handling
├ tests/                 # Unit and integration tests
├ config/                # Configuration files
├ logs/                  # Log files
├ data/                  # Test data and samples
├ main.py               # CLI entry point
├ config.yaml           # Main configuration
├ requirements.txt      # Python dependencies
└ README.md
```

## How It Works

The system follows this pipeline for each file:

1. **File Detection**: Scan folder for supported files
2. **Text Extraction**: Extract text content
3. **Text Cleaning**: Normalize and clean text
4. **Metadata Extraction**: Extract dates, entities, keywords
5. **Classification**: Identify document type
6. **Filename Generation**: Create descriptive filename
7. **Safe Rename**: Rename with conflict resolution
8. **Logging**: Record operation results

## Extending the System

### Adding a Custom Classifier

1. Create a new classifier class in `src/classification/`
2. Inherit from `DocumentClassifier` base class
3. Implement the `classify(text)` method
4. Update `config.yaml` to use your classifier

Example:
```python
from src.classification.base import DocumentClassifier

class MyCustomClassifier(DocumentClassifier):
    def classify(self, text: str) -> dict:
        # Your classification logic
        return {
            'document_type': 'Invoice',
            'confidence': 0.95
        }
```

### Adding a Custom Filename Generator

1. Create a new generator class in `src/naming/`
2. Inherit from `FilenameGenerator` base class
3. Implement the `generate()` method
4. Update `config.yaml` to use your generator

## Testing

Run tests:
```bash
python -m unittest discover tests
```

Run specific test module:
```bash
python -m unittest tests.test_extraction
```

## Error Handling

The system handles various error scenarios:

- **Corrupted files**: Logged and skipped
- **Empty text extraction**: Logged and skipped
- **Classification failures**: Falls back to "Unknown"
- **Permission errors**: Logged and skipped

Check `logs/file_renamer.log` for detailed error information.

## Roadmap

- [ ] Add support for scanned PDFs (OCR)
- [ ] Implement ML-based classifier
- [ ] Add LLM integration (Llama, Mistral)
- [ ] Web interface for easier use
- [ ] Undo/rollback functionality
- [ ] Duplicate detection
- [ ] Watch mode for automatic processing

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please ensure:
- Code follows the modular architecture
- New features include tests
- Documentation is updated

## Support

For issues, questions, or feature requests, please open an issue on the project repository.

## Author

Your Name

## Acknowledgments

Built following offline-first and modular design principles for maximum flexibility and privacy.
