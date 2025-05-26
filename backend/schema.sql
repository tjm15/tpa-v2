-- ENABLE EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;     -- fuzzy text search
CREATE EXTENSION IF NOT EXISTS unaccent;    -- normalize text for search

--------------------------------------------------------------------------------
-- 1. RAW INGESTION LAYER
--------------------------------------------------------------------------------

-- 1.1 Source files (PDF, DOCX, etc.)
CREATE TABLE IF NOT EXISTS source_files (
  id           UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  filename     TEXT      NOT NULL,
  mime_type    TEXT      NOT NULL,
  extension    TEXT,
  uploaded_at  TIMESTAMP DEFAULT timezone('utc', now()),
  storage_path TEXT      NOT NULL,
  source_url   TEXT,
  sha256_hash  TEXT,
  lpa_code     TEXT,
  notes        TEXT
);

-- 1.2 Extracted text chunks (minimal, non-vector)
CREATE TABLE IF NOT EXISTS extracted_text_chunks (
  id           UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  file_id      UUID      NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
  page_number  INTEGER,
  chunk_order  INTEGER   NOT NULL,
  chunk_text   TEXT      NOT NULL,
  created_at   TIMESTAMP DEFAULT timezone('utc', now())
);

--------------------------------------------------------------------------------
-- 2. DOCUMENT STRUCTURE
--------------------------------------------------------------------------------

-- 2.1 Plan documents
CREATE TABLE IF NOT EXISTS plan_documents (
  id              UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  filename        TEXT      NOT NULL,
  name            TEXT      NOT NULL,
  version         TEXT,
  document_status TEXT,
  lpa_code        TEXT,
  created_at      TIMESTAMP DEFAULT timezone('utc', now())
);

-- 2.2 Document node hierarchy
CREATE TABLE IF NOT EXISTS document_nodes (
  id             UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id    UUID      NOT NULL REFERENCES plan_documents(id) ON DELETE CASCADE,
  parent_id      UUID      REFERENCES document_nodes(id),
  title          TEXT      NOT NULL,
  reference      TEXT,
  content        TEXT,
  order_no       INTEGER,
  last_modified  TIMESTAMP,
  author         TEXT
);

--------------------------------------------------------------------------------
-- 3. SPATIAL CONSTRAINTS & SITES
--------------------------------------------------------------------------------

-- 3.1 Constraints (policy‐derived or external)
CREATE TABLE IF NOT EXISTS constraints (
  id               UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
  name             TEXT        NOT NULL,
  type             TEXT        NOT NULL,   -- free‐text or from tags[]
  description      TEXT,
  source_policy_id UUID        REFERENCES policies(id) ON DELETE SET NULL,
  source_document  TEXT,
  geom             GEOMETRY(POLYGON, 4326),
  created_at       TIMESTAMP   DEFAULT timezone('utc', now())
);

-- 3.2 Sites
CREATE TABLE IF NOT EXISTS sites (
  id                       UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  name                     TEXT,
  address                  TEXT,
  uprn                     TEXT,
  lpa_code                 TEXT,
  geom                     GEOMETRY,
  area_ha                  REAL,
  plan_making_status       TEXT[],
  submission_date          DATE,
  source                   TEXT,
  deliverability_assessment JSONB,
  soundness_checks         JSONB,
  created_at               TIMESTAMP DEFAULT timezone('utc', now())
);

--------------------------------------------------------------------------------
-- 4. STRATEGY & GOALS
--------------------------------------------------------------------------------

-- 4.1 Goals
CREATE TABLE IF NOT EXISTS goals (
  id            UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  name          TEXT      NOT NULL,
  category      TEXT[],
  description   TEXT,
  target_metric TEXT,
  target_value  NUMERIC,
  current_value NUMERIC,
  unit          TEXT,
  source        TEXT,
  status        TEXT[],
  type          TEXT[],
  created_at    TIMESTAMP DEFAULT timezone('utc', now())
);

--------------------------------------------------------------------------------
-- 5. POLICY DOMAIN
--------------------------------------------------------------------------------

-- 5.1 Policies (AI-extracted metadata)
CREATE TABLE IF NOT EXISTS policies (
  id                  UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  policy_id           TEXT,        -- e.g. "H1", "DM3" (now nullable)
  policy_title        TEXT      NOT NULL,
  tags                TEXT[],                      -- e.g. ["strategic","SPD"]
  summary             TEXT      NOT NULL,
  -- searchable metadata only:
  cross_references    TEXT[],                      -- codes of other policies
  geographic_mentions TEXT[],
  document_id         UUID      REFERENCES plan_documents(id) ON DELETE SET NULL,
  lpa_code            TEXT,
  created_at          TIMESTAMP DEFAULT timezone('utc', now())
);

-- 5.2 Resolved cross‐policy links (soft references)
CREATE TABLE IF NOT EXISTS policy_cross_links (
  source_policy_code TEXT    NOT NULL,  -- original code
  target_policy_code TEXT    NOT NULL,
  source_policy_id   UUID    REFERENCES policies(id) ON DELETE SET NULL,
  target_policy_id   UUID    REFERENCES policies(id) ON DELETE SET NULL,
  PRIMARY KEY(source_policy_code, target_policy_code)
);

--------------------------------------------------------------------------------
-- 6. HYBRID SEARCH TABLES
--------------------------------------------------------------------------------

-- 6.1 Policy search vectors (semantic + inline metadata)
CREATE TABLE IF NOT EXISTS policy_vectors (
  id                  UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_chunk_id     UUID      NOT NULL REFERENCES extracted_text_chunks(id) ON DELETE CASCADE,
  embedding           vector(768),
  policy_ref          TEXT,      -- e.g. "H1"
  key_themes          TEXT[],
  cross_references    TEXT[],
  geographic_mentions TEXT[],
  tokens              INTEGER,
  model_version       TEXT,      -- track embedding model
  created_at          TIMESTAMP DEFAULT timezone('utc', now())
);
CREATE INDEX IF NOT EXISTS idx_policy_vectors_embedding
  ON policy_vectors USING hnsw (embedding vector_l2_ops);

-- 6.2 Application search vectors
CREATE TABLE IF NOT EXISTS application_vectors (
  id              UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_chunk_id UUID      NOT NULL REFERENCES extracted_text_chunks(id) ON DELETE CASCADE,
  application_id  UUID      REFERENCES planning_applications(id) ON DELETE SET NULL,
  embedding       vector(768),
  document_type   TEXT,
  section_title   TEXT,
  tokens          INTEGER,
  model_version   TEXT,
  created_at      TIMESTAMP DEFAULT timezone('utc', now())
);
CREATE INDEX IF NOT EXISTS idx_application_vectors_embedding
  ON application_vectors USING hnsw (embedding vector_l2_ops);

-- 6.3 Precedent search vectors
CREATE TABLE IF NOT EXISTS precedent_vectors (
  id             UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_case_id UUID      REFERENCES precedent_cases(id) ON DELETE CASCADE,
  embedding      vector(768),
  summary        TEXT,
  key_policies   TEXT[],
  site_context   TEXT,
  model_version  TEXT,
  created_at     TIMESTAMP DEFAULT timezone('utc', now())
);
CREATE INDEX IF NOT EXISTS idx_precedent_vectors_embedding
  ON precedent_vectors USING hnsw (embedding vector_l2_ops);

--------------------------------------------------------------------------------
-- 7. PLANNING APPLICATIONS & AI CONTEXT
--------------------------------------------------------------------------------

-- 7.1 Core application metadata
CREATE TABLE IF NOT EXISTS planning_applications (
  id                 UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  reference_number   TEXT      NOT NULL,
  site_id            UUID      REFERENCES sites(id) ON DELETE SET NULL,
  status             TEXT[],    -- dynamic tags, not rigid enum
  proposal_details   TEXT      NOT NULL,
  received_date      DATE      NOT NULL,
  decision_date      DATE,
  applicant_name     TEXT,
  agent_name         TEXT,
  case_officer       TEXT,
  planner_weightings JSONB,     -- UI-fed overrides
  lpa_code           TEXT,
  created_at         TIMESTAMP DEFAULT timezone('utc', now())
);

-- 7.2 AI reasoning context
CREATE TABLE IF NOT EXISTS application_ai_context (
  application_id    UUID      PRIMARY KEY REFERENCES planning_applications(id) ON DELETE CASCADE,
  retrieval_log_id  UUID      REFERENCES retrieval_logs(log_id),
  reasoning_steps   JSONB,     -- structured trace with step & metadata
  competing_goals   JSONB,
  narrative         TEXT,
  model_version     TEXT,
  created_at        TIMESTAMP DEFAULT timezone('utc', now())
);

-- 7.3 Material references (soft polymorphic)
CREATE TABLE IF NOT EXISTS application_material_refs (
  application_id   UUID NOT NULL REFERENCES planning_applications(id) ON DELETE CASCADE,
  material_type    TEXT NOT NULL,    -- 'policy','constraint','precedent'
  material_code    TEXT NOT NULL,    -- e.g. "H1", free-text if unresolved
  material_id      UUID,             -- nullable FK when resolved
  PRIMARY KEY(application_id, material_type, material_code)
);

--------------------------------------------------------------------------------
-- 8. OFFICER REPORTS (AGENTIC RETRIEVAL)
--------------------------------------------------------------------------------

-- 8.1 Report header
CREATE TABLE IF NOT EXISTS officer_reports (
  application_id   UUID      PRIMARY KEY REFERENCES planning_applications(id) ON DELETE CASCADE,
  ai_context_id    UUID      REFERENCES application_ai_context(application_id),
  version          TEXT      NOT NULL,
  status           TEXT[],   -- dynamic tags
  recommendation   TEXT,
  provenance       JSONB,    -- e.g. { retrieval_log_id, write_log_id }
  created_by       TEXT,
  last_edited_by   TEXT,
  last_modified    TIMESTAMP DEFAULT timezone('utc', now())
);

-- 8.2 Recursive report sections
CREATE TABLE IF NOT EXISTS officer_report_sections (
  application_id    UUID      NOT NULL REFERENCES officer_reports(application_id) ON DELETE CASCADE,
  section_id        UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  parent_section_id UUID,
  title             TEXT      NOT NULL,
  content           TEXT      NOT NULL,
  order_no          INTEGER   NOT NULL,
  agent_stage       TEXT,      -- tag for generation pass
  created_at        TIMESTAMP DEFAULT timezone('utc', now())
);

--------------------------------------------------------------------------------
-- 9. PRECEDENTS
--------------------------------------------------------------------------------

-- 9.1 Precedent cases
CREATE TABLE IF NOT EXISTS precedent_cases (
  id             UUID   PRIMARY KEY DEFAULT uuid_generate_v4(),
  application_id UUID   REFERENCES planning_applications(id) ON DELETE SET NULL,
  case_reference TEXT   NOT NULL,
  address        TEXT,
  decision_date  DATE,
  outcome        TEXT[],
  created_at     TIMESTAMP DEFAULT timezone('utc', now())
);

-- 9.2 Precedent ↔ Policy overlap (soft links)
CREATE TABLE IF NOT EXISTS precedent_key_policies (
  precedent_id UUID NOT NULL REFERENCES precedent_cases(id) ON DELETE CASCADE,
  policy_code  TEXT NOT NULL,
  policy_id    UUID,
  PRIMARY KEY(precedent_id, policy_code)
);

--------------------------------------------------------------------------------
-- 10. AI LOGGING & ENRICHMENT SIDE-CAR
--------------------------------------------------------------------------------

-- 10.1 Retrieval logs
CREATE TABLE IF NOT EXISTS retrieval_logs (
  log_id            UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  timestamp         TIMESTAMP DEFAULT timezone('utc', now()),
  query             TEXT,
  filters           JSONB,
  matched_chunk_ids UUID[],
  retrieval_target  TEXT,      -- e.g. 'policy_vectors'
  agent_context     JSONB
);

-- 10.2 Write logs
CREATE TABLE IF NOT EXISTS write_logs (
  id              UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  timestamp       TIMESTAMP DEFAULT timezone('utc', now()),
  output_type     TEXT      NOT NULL,
  source_entity   TEXT,
  source_id       UUID,
  input_snapshot  JSONB,
  model_version   TEXT,
  output_text     TEXT,
  author          TEXT     DEFAULT 'LLM',
  confidence      FLOAT,
  notes           TEXT
);

-- 10.3 General AI enrichment side-car
CREATE TABLE IF NOT EXISTS ai_enrichment (
  id               UUID      PRIMARY KEY DEFAULT uuid_generate_v4(),
  target_table     TEXT      NOT NULL,
  target_id        UUID      NOT NULL,
  enrichment_type  TEXT      NOT NULL,
  enriched_fields  JSONB     NOT NULL,
  model_version    TEXT,
  created_at       TIMESTAMP DEFAULT timezone('utc', now())
);
CREATE INDEX IF NOT EXISTS idx_ai_enrichment_target
  ON ai_enrichment (target_table, target_id);
