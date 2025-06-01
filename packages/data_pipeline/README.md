# The Planner's Assistant v2 - Data Pipeline

The data pipeline component of The Planner's Assistant v2 (TPA-v2) provides intelligent document ingestion, processing, and knowledge extraction capabilities for planning-related documents. It transforms unstructured planning documents into structured, searchable, and AI-enriched data.

This data pipeline is part of a **monorepo architecture** with shared database models and API schemas, ensuring seamless integration with the backend API and frontend applications.

## Overview

This data pipeline processes planning documents (PDFs, policies, reports) through multiple stages including document parsing, text chunking, AI-powered analysis, policy extraction, spatial designation mapping, and vector embedding generation. The processed data supports both Plan-Making and Development Management planning workflows using shared data models from `libs/shared_db_models/`.

## Monorepo Integration

The data pipeline leverages shared libraries from the monorepo:

- **Database Models**: `../../libs/shared_db_models/` - SQLAlchemy models shared with backend
- **API Schemas**: `../../libs/shared_api_schemas/` - Pydantic models for data validation
- **Utilities**: `../../libs/shared_utils/` - Common utility functions
- **AI Engine**: `../../libs/tpa_ai_engine/` - AI services and agentic retrieval components

All database operations use the same models as the backend API, ensuring data consistency and eliminating model duplication.

## Key Features

- **Document Ingestion**: PDF document processing with text extraction and chunking
- **Policy Extraction**: Automated extraction and structuring of planning policies
- **Vector Embeddings**: High-quality embeddings using BGE-large-en-v1.5 model via HuggingFace
- **Knowledge Graph**: Construction of policy relationships and spatial designation networks
- **Spatial Designation Mapping**: Spatial and semantic spatial designation identification
- **Data Enrichment**: Multi-stage content enhancement and validation
- **Batch Processing**: Efficient processing of large document collections

## Architecture

### Core Components

1. **Orchestrator** (`orchestrator.py`)
   - Main pipeline coordinator
   - Manages document processing workflow
   - Handles batch operations and error recovery

2. **Document Processor** (`document_processor.py`)
   - PDF text extraction and parsing
   - Text chunking and preprocessing
   - Document metadata extraction

3. **Embedder** (`embedder.py`)
   - Vector embedding generation using BGE-large-en-v1.5
   - Batch embedding processing
   - Vector storage and indexing

4. **Policy Extractor** (`policy_extractor.py`)
   - Policy identification and structure analysis
   - Policy metadata extraction
   - Spatial designation detection and classification

5. **Knowledge Graph Builder** (`knowledge_graph.py`)
   - Policy relationship mapping
   - Spatial designation network construction
   - Graph visualization capabilities

### Processing Pipeline

```
PDF Documents → Text Extraction → Chunking → Content Analysis → Policy Extraction
     ↓                                                           ↓
Vector Storage ← Embedding Generation ← Spatial Designation Mapping ← Knowledge Graph
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL with pgvector extension
- HuggingFace account (optional, for embedding generation)
- HuggingFace Transformers library

### Setup

1. **Setup from monorepo root**
   ```bash
   # From tpa-v2/ root directory
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

2. **Navigate to data pipeline**
   ```bash
   cd packages/data_pipeline
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

Note: All required dependencies including shared libraries are installed from the root `pyproject.toml`.

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/tpa_v2
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=tpa_v2

# HuggingFace Services
HF_TOKEN=your_hf_token  # Optional, for private models and enhanced rate limits

# Pipeline Configuration
BATCH_SIZE=50
MAX_CHUNK_SIZE=1000
EMBEDDING_MODEL=BAAI/bge-large-en-v1.5
PROCESSING_WORKERS=4

# File Storage
UPLOAD_DIR=./uploads
PROCESSED_DIR=./processed
LOG_DIR=./logs
```

## Usage

### Running the Pipeline

1. **Basic Document Processing**
   ```bash
   # From packages/data_pipeline with root .venv activated
   python orchestrator.py --input /path/to/documents --output /path/to/processed
   ```

2. **Batch Processing with Configuration**
   ```bash
   python orchestrator.py \
     --input ./documents \
     --batch-size 25 \
     --workers 2 \
     --embedding-model BAAI/bge-large-en-v1.5
   ```

3. **Policy Extraction Only**
   ```bash
   python policy_extractor.py --input processed_documents.json
   ```

4. **Generate Embeddings**
   ```bash
   python embedder.py --input text_chunks.json --model BAAI/bge-large-en-v1.5
   ```

### Data Management Scripts

The `scripts/` directory contains utilities for database operations:

- **Database Setup**: `setup_database.py`
- **Data Import/Export**: `import_export.py`  
- **Data Validation**: `validate_data.py`
- **Cleanup Utilities**: `cleanup.py`

All scripts use shared database models from `../../libs/shared_db_models/` for consistency.

### Processing Workflow

1. **Document Upload**
   - Place PDF documents in the configured upload directory
   - Organize by document type (policies, reports, applications)

2. **Text Extraction**
   - PDF parsing and text extraction
   - Document metadata capture
   - Text preprocessing and cleaning

3. **Chunking**
   - Text segmentation into manageable chunks
   - Chunk overlap for context preservation
   - Metadata association with chunks

4. **Content Analysis**
   - Content classification and tagging
   - Policy identification and extraction
   - Spatial designation detection and mapping

5. **Vector Generation**
   - High-quality embedding generation
   - Vector storage in PostgreSQL with pgvector
   - Indexing for efficient similarity search

6. **Knowledge Graph Construction**
   - Policy relationship identification
   - Spatial designation network mapping
   - Graph visualization and export

## Configuration

### Pipeline Settings

Edit `config/pipeline_config.yaml`:

```yaml
processing:
  batch_size: 50
  max_workers: 4
  chunk_size: 1000
  chunk_overlap: 200

models:
  embedding_model: "BAAI/bge-large-en-v1.5"
  # Add other models for content analysis as needed

storage:
  vector_dimensions: 1024
  similarity_threshold: 0.8
  max_results: 100

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Document Types

The pipeline supports various planning document types:

- **Local Plans**: Strategic planning documents
- **Policies**: Individual planning policies
- **Development Management**: Application guidelines
- **SPDs**: Supplementary Planning Documents
- **Reports**: Planning committee reports
- **Applications**: Planning applications and decisions

## API Integration

The data pipeline integrates with the backend API in `../backend/` for:

- **Document Status Updates**: Processing progress tracking
- **Data Synchronization**: Real-time data updates
- **Search Integration**: Vector search capabilities
- **Knowledge Graph Access**: Policy relationship queries

All integration uses shared database models from `../../libs/shared_db_models/` ensuring data consistency across the entire system.

## Development

### Adding New Document Processors

1. **Create Processor Class**
   ```python
   from libs.shared_db_models.base import BaseDocumentProcessor
   
   class CustomProcessor(BaseDocumentProcessor):
       def process(self, document):
           # Implementation using shared models
           pass
   ```

2. **Register Processor**
   ```python
   # In orchestrator.py
   from .processors.custom_processor import CustomProcessor
   
   PROCESSORS = {
       'custom': CustomProcessor,
       # ... other processors
   }
   ```

### Extending Content Analysis

1. **Custom Analysis Functions**
   ```python
   def custom_analysis(text_chunk):
       # Custom content analysis implementation
       pass
   ```

2. **Integration with Pipeline**
   ```python
   # In policy_extractor.py
   analysis_result = custom_analysis(chunk.text)
   ```

### Testing

```bash
# From packages/data_pipeline with root .venv activated
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_document_processor.py
pytest tests/test_embedder.py
pytest tests/test_policy_extractor.py

# Run with coverage
pytest --cov=ingest_pipeline tests/
```

## Monitoring and Logging

### Log Configuration

Logs are written to:
- `logs/pipeline.log`: General pipeline operations
- `logs/errors.log`: Error and exception tracking
- `logs/performance.log`: Performance metrics

### Monitoring Metrics

- Document processing rates
- HuggingFace API usage and rate limits
- Vector generation performance
- Database operation metrics
- Error rates and types

## Performance Optimization

### Batch Processing

- Configure batch sizes based on available memory
- Use multiprocessing for CPU-intensive tasks
- Implement connection pooling for database operations

### Memory Management

- Process documents in streams for large files
- Clear intermediate data between batches
- Monitor memory usage during processing

### Database Optimization

- Use bulk insert operations
- Implement proper indexing for vector searches
- Regular database maintenance and optimization

## Troubleshooting

### Common Issues

1. **Memory Issues**
   - Reduce batch sizes
   - Increase available system memory
   - Process documents individually for very large files

2. **API Rate Limits**
   - Implement exponential backoff for HuggingFace API
   - Use local models when possible
   - Batch API requests efficiently

3. **Vector Storage Issues**
   - Verify pgvector extension installation
   - Check vector dimensions match model output
   - Ensure proper database permissions

4. **Processing Failures**
   - Check document format compatibility
   - Verify AI service availability
   - Review error logs for specific issues

### Debug Mode

Run with debug logging:
```bash
# From packages/data_pipeline with root .venv activated
python orchestrator.py --debug --input ./documents
```

## Deployment

### Production Setup

1. **Resource Requirements**
   - Minimum 8GB RAM for embedding generation
   - SSD storage for vector operations
   - GPU acceleration recommended for large batches

2. **Container Deployment**
   ```bash
   docker build -t tpa-v2-pipeline .
   docker run -d --name tpa-pipeline \
     -v /path/to/documents:/app/documents \
     -v /path/to/logs:/app/logs \
     --env-file .env \
     tpa-v2-pipeline
   ```

3. **Scheduled Processing**
   ```bash
   # Add to crontab for daily processing
   0 2 * * * cd /path/to/tpa-v2 && source .venv/bin/activate && cd packages/data_pipeline && /path/to/process_daily_documents.sh
   ```

### Scaling Considerations

- Horizontal scaling with multiple worker processes
- Load balancing for API requests
- Distributed vector storage for large datasets
- Caching strategies for frequently accessed data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the coding standards
4. Add tests for new functionality
5. Submit a pull request

## License

This project is part of The Planner's Assistant v2 system. See the main project LICENSE file for details.