# The Planner's Assistant v2 - Backend API

This is the FastAPI backend for The Planner's Assistant v2, providing RESTful APIs for both Plan-Making and Development Management workspaces in the planning domain.

## Overview

The Planner's Assistant v2 is an AI-powered planning support tool that helps planners with:

- **Plan-Making**: Policy development, site allocation, scenario analysis, and plan document management
- **Development Management**: Planning application assessment, precedent analysis, and officer report generation

## Features

### Core API Endpoints

- **Policies** (`/policies`) - Planning policy management and analysis
- **Sites** (`/sites`) - Site allocation and spatial data management
- **Constraints** (`/constraints`) - Planning constraints and spatial overlays
- **Plan Documents** (`/plan-documents`) - Document structure and content management
- **Scenarios** (`/scenarios`) - Alternative development scenario analysis
- **Goals** (`/goals`) - Strategic planning goal tracking
- **Planning Applications** (`/planning-applications`) - Development management workflows
- **Officer Reports** (`/officer-reports`) - AI-assisted report generation
- **Precedent Cases** (`/precedent-cases`) - Case law and precedent analysis
- **AI Services** (`/ai`) - AI-powered guidance and content generation

### Key Capabilities

- **Vector Search**: Semantic search across policies, applications, and precedents using pgvector
- **Spatial Analysis**: PostGIS integration for constraint and site analysis
- **AI Integration**: OpenAI API integration for content generation and analysis
- **Document Processing**: Hierarchical document structure with text chunk extraction
- **Async Operations**: Fully async FastAPI implementation with SQLAlchemy

## Architecture

### Technology Stack

- **Framework**: FastAPI with Pydantic for data validation
- **Database**: PostgreSQL with PostGIS and pgvector extensions
- **ORM**: SQLAlchemy with Alembic for migrations
- **AI/ML**: OpenAI API integration, vector embeddings
- **Background Tasks**: Celery with Redis
- **Development**: Docker containerization

### Database Schema

The system uses a comprehensive PostgreSQL schema with:

- **Document Management**: Source files, text chunks, and document nodes
- **Spatial Data**: Sites, constraints with PostGIS geometry support
- **Planning Domain**: Policies, applications, precedents with cross-references
- **AI Context**: Vector embeddings, retrieval logs, and AI-generated content
- **Reporting**: Officer reports with hierarchical section structure

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL with PostGIS and pgvector extensions
- Redis (for background tasks)
- Docker (recommended for development)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tpa-v2/backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the development server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Docker Development

For containerized development:

```bash
# From the project root
docker-compose up --build
```

This will start:
- FastAPI backend on port 8000
- PostgreSQL database on port 5432
- Redis for background tasks

## Configuration

Configuration is managed through environment variables and the `app/config.py` file:

### Key Settings

- `DATABASE_URL`: PostgreSQL connection string
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`: Database connection details
- `VECTOR_DIM`: Vector embedding dimensions (default: 1024)
- `API_PORT`, `API_HOST`: FastAPI server configuration
- `LOG_LEVEL`: Logging verbosity

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://tpa:tpa@db:5432/tpa
DATABASE_USER=tpa
DATABASE_PASSWORD=tpa
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=tpa
VECTOR_DIM=1024
ENVIRONMENT=development
API_PORT=8000
API_HOST=0.0.0.0
LOG_LEVEL=debug
RELOAD=true
```

## API Documentation

Once the server is running, interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Authentication

Currently, the API runs without authentication for development. Production deployments should implement appropriate authentication and authorization mechanisms.

## Database Migrations

The project uses Alembic for database schema management:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/           # FastAPI route handlers
│   ├── crud/          # Database operations
│   ├── db_models/     # SQLAlchemy models
│   ├── models/        # Pydantic models
│   ├── services/      # Business logic
│   ├── config.py      # Configuration management
│   ├── db.py          # Database connection
│   ├── main.py        # FastAPI application
│   └── utils.py       # Utility functions
├── alembic/           # Database migrations
├── tests/             # Test suite
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration
└── README.md          # This file
```

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **ruff** for linting

Run code quality checks:
```bash
black app/
isort app/
mypy app/
ruff check app/
```

### Testing

Run the test suite:
```bash
pytest tests/
```

## Data Pipeline Integration

The backend integrates with the data pipeline in `../data-pipeline/` for:

- Document ingestion and text extraction
- Policy cross-reference mapping
- Vector embedding generation
- Knowledge graph construction

## Deployment

### Production Considerations

1. **Environment Variables**: Set appropriate production values
2. **Database**: Use managed PostgreSQL with PostGIS and pgvector
3. **Security**: Implement authentication, HTTPS, and input validation
4. **Monitoring**: Add logging, metrics, and health checks
5. **Scaling**: Consider horizontal scaling and load balancing

### Docker Production

Build the production image:
```bash
docker build -t tpa-backend:latest .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run code quality checks
5. Submit a pull request

## License

[Add license information]

## Support

For questions or issues:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the frontend integration guide

---

**Note**: This backend is designed to work with the frontend in `../frontend/` and the data pipeline in `../data-pipeline/`. Ensure all components are properly configured for full functionality.