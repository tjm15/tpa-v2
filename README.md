# The Planner's Assistant v2

The Planner's Assistant v2 (TPA-v2) is an AI-powered planning support tool designed to assist planning authorities with both Plan-Making and Development Management workflows. The system transforms planning documents into structured, searchable data and provides intelligent tools for policy development, site allocation, scenario analysis, and planning application assessment.

## Overview

TPA-v2 consists of three main components that work together to provide comprehensive planning support:

- **Frontend**: Modern web interface built with SvelteKit, providing interactive workspaces for planners
- **Backend**: FastAPI-based REST API with PostgreSQL database and vector search capabilities  
- **Data Pipeline**: Document processing pipeline that transforms PDFs into structured data with embeddings

## Key Features

### Plan-Making Workspace
- **Policy Development**: AI-assisted policy drafting and analysis tools
- **Site Allocation**: Spatial analysis with constraint mapping and policy compliance
- **Scenario Analysis**: Compare alternative development scenarios with trade-off analysis
- **Goal Tracking**: Monitor strategic planning objectives and performance metrics
- **Document Management**: Hierarchical document editing with integrity checks

### Development Management Workspace  
- **Application Assessment**: Intelligent site and proposal evaluation
- **Policy Reasoning**: Step-through analysis linking policies to decisions
- **Precedent Review**: Case law search and comparative analysis
- **Report Generation**: AI-assisted officer report drafting
- **Constraint Analysis**: Automated spatial constraint identification

### AI-Powered Features
- **Vector Search**: Semantic search across policies, applications, and precedents
- **Knowledge Graphs**: Policy relationship mapping and constraint networks
- **Content Generation**: AI-assisted text generation for reports and analysis
- **Spatial Intelligence**: PostGIS integration for geographic analysis

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│    Frontend     │◄──►│     Backend     │◄──►│  Data Pipeline  │
│   (SvelteKit)   │    │    (FastAPI)    │    │   (Python)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   Document      │
                       │  + PostGIS      │    │   Processing    │
                       │  + pgvector     │    │   & Embeddings  │
                       └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Frontend**: SvelteKit, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL with PostGIS and pgvector
- **Data Pipeline**: Python, HuggingFace Transformers, BGE-large-en-v1.5 embeddings
- **Database**: PostgreSQL with spatial (PostGIS) and vector (pgvector) extensions
- **Infrastructure**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for data pipeline development)

### Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd tpa-v2
   ```

2. **Start the Database**
   ```bash
   docker-compose up postgres -d
   ```

3. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Run database migrations
   alembic upgrade head
   
   # Start the API server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Setup Data Pipeline** (Optional)
   ```bash
   cd data-pipeline
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Configure environment variables
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Using Docker Compose

For a complete containerized setup:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Database: localhost:5432

## Project Structure

```
tpa-v2/
├── frontend/                 # SvelteKit web application
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/   # Reusable UI components
│   │   │   ├── services/     # API clients and data services
│   │   │   ├── stores/       # Application state management
│   │   │   └── types/        # TypeScript type definitions
│   │   └── routes/           # Page components and routing
│   ├── package.json
│   └── README.md
├── backend/                  # FastAPI REST API
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   ├── crud/             # Database operations
│   │   ├── db_models/        # SQLAlchemy database models
│   │   ├── models/           # Pydantic request/response models
│   │   └── services/         # Business logic services
│   ├── alembic/              # Database migration files
│   ├── requirements.txt
│   └── README.md
├── data-pipeline/            # Document processing pipeline
│   ├── ingest_pipeline/      # Core pipeline modules
│   │   ├── orchestrator.py   # Main pipeline coordinator
│   │   ├── embedder.py       # Vector embedding generation
│   │   ├── models.py         # Database models
│   │   └── *.py              # Processing modules
│   ├── scripts/              # Utility scripts
│   ├── requirements.txt
│   └── README.md
├── docker-compose.yml        # Multi-service container setup
└── README.md                 # This file
```

## Database Schema

The system uses a comprehensive PostgreSQL schema supporting:

- **Document Management**: Source files, text chunks, document hierarchies
- **Planning Domain**: Policies, sites, constraints, applications, precedents
- **Spatial Data**: PostGIS geometries for sites and constraints  
- **Vector Storage**: pgvector embeddings for semantic search
- **AI Context**: Reasoning traces, material references, enrichments
- **Reporting**: Officer reports with hierarchical sections

Key tables include:
- `policies`, `sites`, `constraints`, `planning_applications`
- `extracted_text_chunks`, `policy_vectors`, `application_vectors`
- `scenarios`, `goals`, `precedent_cases`, `officer_reports`

## API Documentation

The backend provides RESTful APIs for all major entities:

- **Policies** (`/policies`) - Policy management and analysis
- **Sites** (`/sites`) - Site allocation and spatial data
- **Constraints** (`/constraints`) - Planning constraints and overlays
- **Planning Applications** (`/planning-applications`) - Application workflows
- **Scenarios** (`/scenarios`) - Plan scenario analysis  
- **Goals** (`/goals`) - Strategic objective tracking
- **AI Services** (`/ai`) - AI-powered content generation

Full API documentation is available at `/docs` when running the backend.

## Data Processing Pipeline

The data pipeline transforms planning documents through:

1. **Document Ingestion**: PDF parsing and text extraction
2. **Text Chunking**: Segmentation with metadata preservation  
3. **Policy Extraction**: Automated policy identification and structuring
4. **Vector Generation**: BGE-large-en-v1.5 embeddings via HuggingFace
5. **Knowledge Graph**: Policy relationship and constraint mapping
6. **Database Storage**: Structured data with vector indexing

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Frontend Development

```bash
cd frontend

# Development server with hot reload
npm run dev

# Type checking
npm run check

# Format code
npm run format

# Build for production
npm run build
```

### Data Pipeline Development

```bash
cd data-pipeline
source venv/bin/activate

# Process documents
python ingest_pipeline/orchestrator.py --input ./documents

# Generate embeddings
python ingest_pipeline/embedder.py --input chunks.json

# Run tests
pytest tests/
```

## Configuration

### Environment Variables

Create `.env` files in each component directory:

**Backend** (`.env`):
```env
DATABASE_URL=postgresql://tpa_user:tpa_password@localhost:5432/tpa_db
POSTGRES_USER=tpa_user
POSTGRES_PASSWORD=tpa_password
POSTGRES_DB=tpa_db
```

**Data Pipeline** (`.env`):
```env
DATABASE_URL=postgresql://tpa_user:tpa_password@localhost:5432/tpa_db
HF_TOKEN=your_huggingface_token
EMBEDDING_MODEL=BAAI/bge-large-en-v1.5
BATCH_SIZE=50
```

### Docker Configuration

The `docker-compose.yml` file provides:
- PostgreSQL with pgvector and PostGIS extensions
- Backend API service with auto-restart
- Frontend development server
- Volume mounts for development

## Deployment

### Production Deployment

1. **Database Setup**
   ```bash
   # Setup PostgreSQL with required extensions
   CREATE EXTENSION IF NOT EXISTS postgis;
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

2. **Backend Deployment**
   ```bash
   cd backend
   docker build -t tpa-backend .
   docker run -d --name tpa-backend \
     -p 8000:8000 \
     --env-file .env \
     tpa-backend
   ```

3. **Frontend Deployment**
   ```bash
   cd frontend
   npm run build
   # Deploy dist/ directory to your web server
   ```

### Environment-Specific Configuration

- **Development**: Use Docker Compose with hot reload
- **Staging**: Container deployment with external database
- **Production**: Orchestrated deployment with load balancing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the coding standards
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Standards

- **Backend**: Follow PEP 8, use type hints, write docstrings
- **Frontend**: Use TypeScript, follow Svelte conventions, use Prettier
- **Data Pipeline**: Document functions, handle errors gracefully
- **General**: Write meaningful commit messages, add tests

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Start all services
docker-compose up -d

# Run integration test suite
./scripts/run_integration_tests.sh
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running and accessible
   - Check DATABASE_URL environment variable
   - Ensure pgvector and PostGIS extensions are installed

2. **Vector Search Issues**
   - Confirm pgvector extension is loaded
   - Check embedding dimensions match model output (1024 for BGE-large-en-v1.5)
   - Verify HuggingFace token for embedding generation

3. **Frontend API Errors**
   - Ensure backend is running on expected port
   - Check CORS configuration for development
   - Verify API endpoint URLs in frontend configuration

### Performance Optimization

- **Database**: Create proper indexes for frequent queries
- **Vector Search**: Use appropriate similarity thresholds
- **Embedding Generation**: Batch process documents efficiently
- **Frontend**: Implement pagination for large datasets

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions:

1. Check existing [Issues](../../issues) for similar problems
2. Create a new issue with detailed description
3. For development questions, see component-specific README files:
   - [Backend README](backend/README.md)
   - [Frontend README](frontend/README.md)  
   - [Data Pipeline README](data-pipeline/README.md)