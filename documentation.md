# AI File Renamer — Development Specification (Offline, Text-Based Only)

---

## 1. Project Scope

### 1.1 Functional Requirements

The system MUST:

- Detect files inside a target folder
- Filter supported file extensions
- Extract textual content from files
- Clean extracted text
- Classify document content
- Generate a filename based on extracted information
- Rename the original file safely

---

### 1.2 Non-Functional Requirements

The system MUST be:

- Fully offline
- Modular and replaceable (AI module must be swappable)
- Safe (must never overwrite files without conflict handling)
- Loggable (all operations must be traceable)

---

### 1.3 Supported File Types (Current Version)

The system MUST support:

```

.pdf (text-based PDFs only)
.txt
.docx

```

The system MUST NOT support:

```

Scanned PDFs
Images

```

---

## 2. System Pipeline

The system MUST execute the following pipeline for each file:

```

Folder Scan
→ Extension Filter
→ Text Extraction
→ Text Cleaning
→ Document Classification
→ Metadata Extraction
→ Filename Generation
→ Safe File Rename
→ Logging

```

---

## 3. Project Structure

The project MUST follow this structure:

```

ai-file-renamer/
│
├ src/
│   ├ core/
│   ├ extraction/
│   ├ cleaning/
│   ├ classification/
│   ├ naming/
│   ├ utils/
│
├ tests/
├ config/
├ logs/
├ data/
│
├ main.py
├ requirements.txt
├ config.yaml
└ README.md
```

#### Dependencies (requirements.txt)

Minimum required packages:

```
pypdf>=4.0.0          # PDF text extraction
python-docx>=1.0.0    # DOCX text extraction
python-dateutil>=2.8.0 # Date parsing
pyyaml>=6.0           # Configuration
```

Optional packages (for swappable components):

```
# For ML classification
scikit-learn>=1.3.0
joblib>=1.3.0

# For LLM-based solutions
transformers>=4.30.0
torch>=2.0.0

# For advanced NER
spacy>=3.5.0
```


---

## 4. Module Specifications

---

### 4.1 File Detection Module

#### Responsibilities

- Scan target directory
- Detect files recursively (optional but recommended)
- Filter supported extensions
- Ignore already processed files (if tracking enabled)

#### Required Functions

```

scan_folder(path) → list[file_paths]
filter_supported_files(file_list) → list[file_paths]

````

#### Supported Extensions Configuration

```python
SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".txt",
    ".docx"
]
````

---

### 4.2 Text Extraction Module

#### Responsibilities

* Extract text from supported files
* Detect non-text PDFs and reject them
* Provide unified extraction interface

#### Required Functions

```
extract_text(file_path) → raw_text
extract_pdf_text(file_path) → raw_text
extract_txt_text(file_path) → raw_text
extract_docx_text(file_path) → raw_text
```

#### Requirements

##### PDF extraction MUST:

* Detect if PDF contains selectable text
* Return None and log error if not text-based

##### TXT extraction MUST:

* Support UTF-8
* Handle encoding fallback safely

##### DOCX extraction MUST:

* Extract all paragraph text
* Ignore formatting safely
* Handle empty documents

---

### 4.3 Text Cleaning Module

#### Responsibilities

Normalize extracted text for downstream processing.

#### Cleaning Rules

The module MUST:

* Remove extra whitespace
* Normalize line breaks
* Remove non-printable characters
* Trim leading and trailing spaces

#### Required Functions

```
clean_text(raw_text) → cleaned_text
normalize_whitespace(text) → text
remove_special_characters(text) → text
```

---

### 4.4 Metadata Extraction Module

#### Responsibilities

Extract structured information from cleaned text.

#### Required Extracted Fields

The system SHOULD attempt to extract (with priority order):

```
1. date (REQUIRED - use file modified date as fallback)
2. organization_name (optional)
3. person_name (optional)
4. document_keywords (optional, max 2-3 keywords)
```

#### Required Functions

```
extract_dates(text) → list[dates]
extract_entities(text) → dict
```

#### Date Formats Supported

**Input formats** (parsing from documents):
```
DD/MM/YYYY
YYYY-MM-DD
Month YYYY
DD-MM-YYYY
MM/DD/YYYY
```

**Output format** (for filenames):
```
YYYY-MM-DD (for sortability and consistency)
```

---

### 4.5 Document Classification Module

**⚠️ NOTE: This module is FULLY SWAPPABLE. The implementation below is a reference solution. You can replace this entirely with any alternative approach (AI-based, LLM-based, ML-based, etc.) as long as it follows the interface contract.**

#### Responsibilities

Classify document type based on text content.

#### Interface Contract (REQUIRED)

```python
class DocumentClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> dict:
        """
        Returns:
        {
            "document_type": str,
            "confidence": float (0.0 to 1.0)
        }
        """
        pass
```

#### Reference Implementation: Rule-Based Keyword Matching

The initial classifier uses rule-based keyword matching.

**Confidence Score Mapping:**
```
Exact keyword match (multiple keywords) → 0.9
Partial match (single keyword) → 0.6
Weak indicators → 0.3
No match (fallback to "Unknown") → 0.1
```

**Example Rules:**

```
IF "invoice" AND "amount" IN text → Invoice (confidence: 0.9)
IF "passport" IN text → ID (confidence: 0.6)
IF "statement" AND "bank" IN text → Bank Statement (confidence: 0.9)
ELSE → Unknown (confidence: 0.1)
```

---

### 4.6 Filename Generation Module

**⚠️ NOTE: This module is FULLY SWAPPABLE. The implementation below is a reference solution. You can replace this entirely with any alternative approach (template-based, AI-generated, custom logic, etc.) as long as it follows the interface contract.**

#### Responsibilities

Generate structured filename using metadata and classification.

#### Interface Contract (REQUIRED)

```python
class FilenameGenerator(ABC):
    @abstractmethod
    def generate(self, metadata: dict, classification: dict, original_filename: str) -> str:
        """
        Returns: sanitized filename (without extension)
        """
        pass
```

#### Reference Implementation: Template-Based Generation

**Primary Template Format:**

```
{DocumentType}_{PrimaryEntity}_{Date}
```

**Fallback Logic:**

```
IF all fields available → {DocumentType}_{PrimaryEntity}_{Date}
IF date missing → {DocumentType}_{PrimaryEntity}_{FileModifiedDate}
IF entity missing → {DocumentType}_{Date}
IF all metadata missing → {DocumentType}_NoMetadata_{Timestamp}
IF classification failed → Unknown_{Date}
IF all failed → Original_{Timestamp}
```

#### Required Functions

```
generate_filename(metadata, classification, original_filename) → str
sanitize_filename(filename) → str
apply_fallback_logic(metadata, classification) → str
```

#### Sanitization Rules

Remove/replace characters:

```
/ \ : * ? " < > |
Replace spaces with underscores
Remove leading/trailing dots and underscores
```

#### Length Constraints

Maximum filename length MUST be:

```
150 characters (excluding extension)
If exceeded, truncate from middle and add "..."
```

---

### 4.7 Safe Rename Module

#### Responsibilities

Rename files without overwriting existing files.

#### Required Functions

```
rename_file(original_path, new_filename) → new_path
resolve_name_conflicts(target_path) → safe_path
```

#### Conflict Resolution Rule

If filename exists:

```
file.pdf
file_v2.pdf
file_v3.pdf
```

---

### 4.8 Logging Module

#### Responsibilities

Log all operations.

#### Log Format

**Format:** JSON (for easy parsing) or structured text

**Example JSON log entry:**
```json
{
  "timestamp": "2026-02-16T10:30:45.123Z",
  "level": "INFO",
  "original_filename": "document.pdf",
  "generated_filename": "Invoice_AcmeCorp_2026-02-15.pdf",
  "classification": {"type": "Invoice", "confidence": 0.9},
  "status": "success",
  "error": null
}
```

#### Log Entries MUST Include

```
timestamp (ISO 8601 format)
level (DEBUG, INFO, WARNING, ERROR)
original filename
generated filename (if applicable)
classification result (type + confidence)
metadata extracted
status (success, skipped, failed)
error message (if applicable)
processing time (milliseconds)
```

#### Log Levels

```
DEBUG: Detailed processing steps
INFO: Successful renames
WARNING: Skipped files, fallback usage
ERROR: Failures, exceptions
```

---

## 5. CLI Interface

### Command Format

```
rename-ai <folder_path>
```

### Optional Flags

```
--preview     Show rename results without renaming
--verbose     Show detailed logs
```

---

## 6. Error Handling Requirements

The system MUST handle:

* **Corrupted files** → Log error, skip file, continue processing
* **Empty extracted text** → Log warning, attempt classification with filename, or skip
* **Extraction failures** → Log error with stack trace, skip file, continue processing
* **Rename permission errors** → Log error, notify user, skip file, continue processing
* **Classification failures** → Log warning, use fallback ("Unknown"), continue processing
* **Filename generation failures** → Log error, use fallback template, continue processing

#### Error Handling Policy

**Default Policy:** Log error, skip problematic file, continue batch processing

**Critical Errors (halt processing):**
* Target folder does not exist or is not accessible
* No write permissions for entire target folder
* Disk full

**Recoverable Errors (skip and continue):**
* Individual file extraction failures
* Individual file rename failures
* Classification/naming failures

---

## 7. Testing Requirements

### Unit Tests MUST Cover

* Text extraction
* Text cleaning
* Date extraction
* Filename generation

---

### Integration Tests MUST Cover

Full pipeline:

```
Input file → Correct renamed output file
```

---

## 8. Modularity and Swappable Components

### 8.1 Core Pipeline (Fixed)

The following pipeline stages are FIXED and mandatory:

```
1. File Detection
2. Text Extraction  
3. Text Cleaning
4. Metadata Extraction
```

### 8.2 Swappable Components (Pluggable)

The following components are FULLY SWAPPABLE and can be replaced without modifying other modules:

#### **Classification Module** (Section 4.5)

Can be replaced with:
* Rule-based keyword matching (reference implementation)
* Local ML classifier (scikit-learn, etc.)
* Local LLM (Llama, Mistral, etc.)
* Transformer models (BERT-based classification)
* Hybrid approach
* External API (if offline requirement is relaxed)

#### **Filename Generation Module** (Section 4.6)

Can be replaced with:
* Template-based (reference implementation)
* AI-generated filenames using LLM
* Custom business logic
* User-defined patterns via config
* Dynamic templates based on document type

### 8.3 Interface Contracts

All swappable components MUST implement the defined interface contracts (see sections 4.5 and 4.6).

**Design Principle:** The core pipeline should pass extracted text and metadata to the swappable components and receive structured output, without knowing implementation details.

### 8.4 Configuration

The active implementation MUST be selectable via configuration:

```yaml
classifier:
  type: "rule_based"  # or "ml", "llm", "transformer"
  
filename_generator:
  type: "template"    # or "ai", "custom"
```

---

## 9. Execution Flow Specification

For each file:

```
1. Scan folder
2. Filter supported extension
3. Extract text
4. Clean text
5. Extract metadata
6. Classify document
7. Generate filename
8. Sanitize filename
9. Resolve conflicts
10. Rename file
11. Log result
```

---

## 10. Acceptance Criteria

The system is considered complete when:

* Successfully processes batch folder
* Renames files correctly
* Handles conflicts safely
* Runs fully offline
* Logs all operations

