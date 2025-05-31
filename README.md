# The Planner's Assistant v2

The Planner's Assistant v2 (TPA-v2) is an AI-powered planning support tool designed to assist planning authorities with both Plan-Making and Development Management workflows. The system transforms planning documents into structured, searchable data and provides intelligent tools for policy development, site allocation, scenario analysis, and planning application assessment.

## Overview

TPA-v2 is built as a modular **monorepo** with shared libraries that enable maintainable, scalable development. The system consists of:

- **Applications** (`packages/`): Deployable frontend, backend, and data pipeline services
- **Shared Libraries** (`libs/`): Reusable models, schemas, utilities, and AI components  
- **Documentation** (`docs/`): Project-wide documentation and guides
- **Root Configuration**: Centralized database migrations, environment, and project setup

### Core Components

- **Frontend** (`packages/frontend/`): Modern web interface built with SvelteKit
- **Backend** (`packages/backend/`): FastAPI-based REST API with PostgreSQL database  
- **Data Pipeline** (`packages/data_pipeline/`): Document processing pipeline with AI enrichment
- **Shared Libraries** (`libs/`): Common database models, API schemas, utilities, and AI engine

## Monorepo Architecture

```
tpa-v2/
├── packages/           # Deployable applications
│   ├── frontend/      # SvelteKit web application
│   ├── backend/       # FastAPI REST API
│   └── data_pipeline/ # Document processing pipeline
├── libs/              # Shared libraries
│   ├── shared_db_models/     # SQLAlchemy database models
│   ├── shared_api_schemas/   # Pydantic request/response models
│   ├── shared_utils/         # Common utilities
│   └── tpa_ai_engine/       # AI components and services
├── docs/              # Project documentation
├── root_alembic/      # Database migrations (shared across all apps)
└── pyproject.toml     # Python workspace configuration
```

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
│    Frontend     │◄──►│     Backend     │◄──►│  Data Pipeline  │
│   (SvelteKit)   │    │    (FastAPI)    │    │   (Python)      │
│ packages/       │    │ packages/       │    │ packages/       │
│ frontend/       │    │ backend/        │    │ data_pipeline/  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   Document      │
                       │  + PostGIS      │    │   Processing    │
                       │  + pgvector     │    │   & Embeddings  │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────────────────────────────┐
                       │           Shared Libraries              │
                       │  libs/shared_db_models/      Database   │
                       │  libs/shared_api_schemas/    API Models │
                       │  libs/shared_utils/          Utilities  │
                       │  libs/tpa_ai_engine/         AI Engine  │
                       └─────────────────────────────────────────┘
```

### Technology Stack

- **Frontend**: SvelteKit, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL with PostGIS and pgvector
- **Data Pipeline**: Python, HuggingFace Transformers, BGE-large-en-v1.5 embeddings
- **Database**: PostgreSQL with spatial (PostGIS) and vector (pgvector) extensions
- **Infrastructure**: Docker, Docker Compose
- **Architecture**: Monorepo with shared Python libraries for models, schemas, and utilities

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend and data pipeline development)

### Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd tpa-v2
   ```

2. **Setup Python Environment (Root Level)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Start the Database**
   ```bash
   docker-compose up postgres -d
   ```

4. **Run Database Migrations**
   ```bash
   # From the root directory with activated venv
   alembic -c root_alembic.ini upgrade head
   ```

5. **Start Backend**
   ```bash
   cd packages/backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Start Frontend**
   ```bash
   cd packages/frontend
   npm install
   npm run dev
   ```

7. **Setup Data Pipeline** (Optional)
   ```bash
   cd packages/data_pipeline
   # The shared dependencies are already available from root venv
   
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
tpa-v2/                       # Monorepo root
├── packages/                 # Deployable applications
│   ├── frontend/            # SvelteKit web application
│   │   ├── src/
│   │   │   ├── lib/
│   │   │   │   ├── components/   # UI components
│   │   │   │   ├── services/     # API clients
│   │   │   │   ├── stores/       # State management
│   │   │   │   └── types/        # TypeScript types
│   │   │   └── routes/           # Page components
│   │   ├── package.json
│   │   └── README.md
│   ├── backend/             # FastAPI REST API
│   │   ├── app/
│   │   │   ├── api/             # API route handlers
│   │   │   ├── crud/            # Database operations
│   │   │   └── services/        # Business logic
│   │   ├── requirements.txt
│   │   └── README.md
│   └── data_pipeline/       # Document processing pipeline
│       ├── ingest_pipeline/ # Core pipeline modules
│       ├── scripts/         # Processing scripts
│       ├── requirements.txt
│       └── README.md
├── libs/                    # Shared libraries
│   ├── shared_db_models/    # SQLAlchemy database models
│   ├── shared_api_schemas/  # Pydantic request/response models
│   ├── shared_utils/        # Common utilities
│   └── tpa_ai_engine/       # AI components and services
├── docs/                    # Project documentation
│   ├── architecture.md
│   ├── setup_guide.md
│   └── ux_design_approach.md
├── root_alembic/           # Database migrations (shared)
│   ├── env.py
│   ├── versions/
│   └── script.py.mako
├── pyproject.toml          # Python workspace configuration
├── root_alembic.ini        # Alembic configuration
├── docker-compose.yml      # Multi-service container setup
└── README.md               # This file
```

## Database Schema

The system uses a comprehensive PostgreSQL schema supporting:

- **Document Management**: Source files, text chunks, document hierarchies
- **Planning Domain**: Policies, sites, constraints, applications, precedents
- **Spatial Data**: PostGIS geometries for sites and constraints  
- **Vector Storage**: pgvector embeddings for semantic search
- **AI Context**: Reasoning traces, material references, enrichments
- **Reporting**: Officer reports with hierarchical sections

All database models are centralized in `libs/shared_db_models/` for consistency across applications.

Key shared models include:
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
# From root directory with activated venv
cd packages/backend

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Database migrations (from root)
cd ../../
alembic -c root_alembic.ini revision --autogenerate -m "Description"
alembic -c root_alembic.ini upgrade head
```

### Frontend Development

```bash
cd packages/frontend

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
# From root directory with activated venv
cd packages/data_pipeline

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

Note: All applications now use shared database models from `libs/shared_db_models/` and API schemas from `libs/shared_api_schemas/`.

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
   cd packages/backend
   docker build -t tpa-backend .
   docker run -d --name tpa-backend \
     -p 8000:8000 \
     --env-file .env \
     tpa-backend
   ```

3. **Frontend Deployment**
   ```bash
   cd packages/frontend
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
# From root with activated venv
cd packages/backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd packages/frontend
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

This project is licensed under the AGPLv3 License - see the [LICENSE](LICENSE) file for details.

## Support

For questions, issues, or contributions:

1. Check existing [Issues](../../issues) for similar problems
2. Create a new issue with detailed description
3. For development questions, see component-specific README files:
   - [Backend README](packages/backend/README.md)
   - [Frontend README](packages/frontend/README.md)  
   - [Data Pipeline README](packages/data_pipeline/README.md)
