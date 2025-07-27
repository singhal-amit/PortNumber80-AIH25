# Challenge 1a: PDF Processing Solution

## Overview
This is a **sample solution** for Challenge 1a of the Adobe India Hackathon 2025. The challenge requires implementing a PDF processing solution that extracts structured data from PDF documents and outputs JSON files. The solution must be containerized using Docker and meet specific performance and resource constraints.

## Official Challenge Guidelines

### Submission Requirements
- **GitHub Project**: Complete code repository with working solution
- **Dockerfile**: Must be present in the root directory and functional
- **README.md**:  Documentation explaining the solution, models, and libraries used

## Testing Solution

```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-processor .

# Test with sample data
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdf-processor
```

## Solution_1a Structure
```
📁 Solution_1a/                       # Challenge 1a: PDF Processing Solution
├── 📄 Dockerfile                         # Container configuration for PDF processing
├── 📄 process_pdfs.py                    # Main PDF processing script
├── 📄 README.md                          # Solution 1a documentation
├── 📄 requirements.txt                   # Python dependencies
│
├── 📁 debug/                             # Debugging utilities
|    ├── 🐛 debug_pdf.py        
|    └── 🐛 debug_title.py     
│
├── 📁 local_model/                       # Local ML model
|    └── 📁 models--prajjwal1--bert-tiny/  
│
├── 📁 pdf_outliner/                      # Core PDF processing module
|    └── 📄 extractor.py                       # PDF content extraction logic
│
├── 📁 sample_dataset/                    # Test dataset for validation
|    ├── 📁 expected_outputs/                  # Expected JSON outputs
|    ├── 📁 outputs/                           # Generated JSON outputs
|    ├── 📁 pdfs/                              # Sample PDF input files
|    └── 📁 schema/                            # Output format specifications
|         └── 📄 output_schema.json
│
└── 📁 tests/                             # Unit tests and validation
    └── 📄 test_solution.py                    # Test suite for Solution 1a
```

## Implementation

### Current Sample Solution
The provided `process_pdfs.py` is a **basic sample** that demonstrates:
- PDF file scanning from input directory
- Dummy JSON data generation
- Output file creation in the specified format

**Note**: This is a placeholder implementation using dummy data. A real solution would need to:
- Implement actual PDF text extraction
- Parse document structure and hierarchy
- Generate meaningful JSON output based on content analysis

### Critical Constraints
- **Execution Time**: ≤ 10 seconds for a 50-page PDF
- **Model Size**: ≤ 200MB (if using ML models)
- **Network**: No internet access allowed during runtime execution
- **Runtime**: Must run on CPU (amd64) with 8 CPUs and 16 GB RAM
- **Architecture**: Must work on AMD64, not ARM-specific

### Key Requirements
- **Automatic Processing**: Process all PDFs from `/app/input` directory
- **Output Format**: Generate `filename.json` for each `filename.pdf`
- **Input Directory**: Read-only access only
- **Open Source**: All libraries, models, and tools must be open source
- **Cross-Platform**: Test on both simple and complex PDFs

## Implementation Guidelines

### Performance Considerations
- **Memory Management**: Efficient handling of large PDFs
- **Processing Speed**: Optimize for sub-10-second execution
- **Resource Usage**: Stay within 16GB RAM constraint
- **CPU Utilization**: Efficient use of 8 CPU cores

### Testing Strategy
- **Simple PDFs**: Test with basic PDF documents
- **Complex PDFs**: Test with multi-column layouts, images, tables
- **Large PDFs**: Verify 50-page processing within time limit

### Validation Checklist
- [ ] All PDFs in input directory are processed
- [ ] JSON output files are generated for each PDF
- [ ] Output format matches required structure
- [ ] **Output conforms to schema** in `sample_dataset/schema/output_schema.json`
- [ ] Processing completes within 10 seconds for 50-page PDFs
- [ ] Solution works without internet access
- [ ] Memory usage stays within 16GB limit
- [ ] Compatible with AMD64 architecture
