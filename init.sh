#!/usr/bin/env bash
set -e

echo "Creating folder structure…"

# Root files
touch .gitignore .env.example README.md docker-compose.yml

# scripts/
mkdir -p scripts
touch scripts/init_db.sh scripts/generate_docs.sh

# backend/
mkdir -p backend/alembic
mkdir -p backend/app/core backend/app/db \
         backend/app/api/v1/routers backend/app/services \
         backend/app/tasks backend/app/utils \
         backend/tests
touch backend/Dockerfile backend/requirements.txt
touch backend/app/__init__.py backend/app/main.py
touch backend/app/core/config.py backend/app/core/security.py
touch backend/app/db/session.py backend/app/db/base.py
touch backend/app/api/v1/routers/assessment.py \
      backend/app/api/v1/routers/policy.py \
      backend/app/api/v1/routers/allocation.py
touch backend/app/api/v1/schemas.py backend/app/api/v1/dependencies.py
touch backend/app/services/constraint_service.py \
      backend/app/services/policy_service.py \
      backend/app/services/reasoning_service.py \
      backend/app/services/graph_service.py
touch backend/app/tasks/celery_app.py backend/app/tasks/reasoning_tasks.py
touch backend/app/utils/geo.py backend/app/utils/embeddings.py
touch backend/tests/conftest.py backend/tests/test_placeholder.py

# data_pipeline/
mkdir -p data_pipeline/python data_pipeline/configs data_pipeline/notebooks
touch data_pipeline/python/pdf_extract.py \
      data_pipeline/python/vector_index.py \
      data_pipeline/python/graph_builder.py

# frontend/
mkdir -p frontend/public \
         frontend/src/config \
         frontend/src/components/MapView \
         frontend/src/components/PolicyCard \
         frontend/src/components/ReasoningPanel \
         frontend/src/pages \
         frontend/src/services \
         frontend/src/hooks \
         frontend/src/styles \
         frontend/src/utils
touch frontend/Dockerfile frontend/package.json \
      frontend/tsconfig.json frontend/tailwind.config.js
touch frontend/src/App.tsx frontend/src/index.tsx
touch frontend/src/pages/AssessmentPage.tsx \
      frontend/src/pages/DraftPolicyPage.tsx

# docs/
mkdir -p docs/v3_data_flow_diagrams
touch docs/v3_graph_schema.png docs/ux_data_contract_matrix.md

echo "✅ Folder structure created!"
