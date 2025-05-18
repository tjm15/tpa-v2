#!/usr/bin/env bash
set -euo pipefail

DB_DIR="app/db_models"

mkdir -p "$DB_DIR"

touch "$DB_DIR/__init__.py"
touch "$DB_DIR/base.py"

models=(
  policies
  sites
  constraints
  plan_documents
  scenarios
  goals
  planning_applications
  officer_reports
  precedent_cases
)

for model in "${models[@]}"; do
  touch "$DB_DIR/${model}.py"
done

echo "✅ db_models/ structure created:"
tree "$DB_DIR"
