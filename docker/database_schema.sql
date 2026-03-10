Get-Content database_schema.sql | docker exec -i autosage-postgres psql -U postgres -d autosage


-- =====================================================
-- EXTENSION
-- =====================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- =====================================================
-- AGENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS agents (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    temperature DOUBLE PRECISION NULL,
    max_tokens INTEGER NULL,
    use_rag BOOLEAN NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,

    CONSTRAINT uq_agents_name UNIQUE (name)
);

-- =====================================================
-- DOCUMENT CHUNKS (RAG)
-- =====================================================

CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    chunk_metadata JSON NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,

    CONSTRAINT uq_document_chunks_agent_content
        UNIQUE (agent_id, content),

    CONSTRAINT fk_document_chunks_agent
        FOREIGN KEY (agent_id)
        REFERENCES agents (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_document_chunks_agent_id
    ON document_chunks(agent_id);

CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding
    ON document_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- =====================================================
-- PIPELINES
-- =====================================================

CREATE TABLE IF NOT EXISTS pipelines (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,

    CONSTRAINT uq_pipelines_name UNIQUE (name)
);

-- =====================================================
-- PIPELINE VERSIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS pipeline_versions (
    id VARCHAR PRIMARY KEY,
    pipeline_id VARCHAR NOT NULL,
    version_number INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,

    CONSTRAINT uq_pipeline_version_number
        UNIQUE (pipeline_id, version_number),

    CONSTRAINT fk_pipeline_versions_pipeline
        FOREIGN KEY (pipeline_id)
        REFERENCES pipelines (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pipeline_versions_pipeline_id
    ON pipeline_versions(pipeline_id);

-- =====================================================
-- PIPELINE NODES
-- =====================================================

CREATE TABLE IF NOT EXISTS pipeline_nodes (
    id VARCHAR PRIMARY KEY,
    version_id VARCHAR NOT NULL,
    node_id VARCHAR NOT NULL,
    agent_id VARCHAR NOT NULL,

    CONSTRAINT uq_pipeline_nodes_version_node
        UNIQUE (version_id, node_id),

    CONSTRAINT fk_pipeline_nodes_version
        FOREIGN KEY (version_id)
        REFERENCES pipeline_versions (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pipeline_nodes_agent
        FOREIGN KEY (agent_id)
        REFERENCES agents (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pipeline_nodes_version_id
    ON pipeline_nodes(version_id);

CREATE INDEX IF NOT EXISTS idx_pipeline_nodes_agent_id
    ON pipeline_nodes(agent_id);

-- =====================================================
-- PIPELINE EDGES
-- =====================================================

CREATE TABLE IF NOT EXISTS pipeline_edges (
    id VARCHAR PRIMARY KEY,
    version_id VARCHAR NOT NULL,
    source_node_id VARCHAR NOT NULL,
    target_node_id VARCHAR NOT NULL,
    condition_json JSON NULL,

    CONSTRAINT fk_pipeline_edges_version
        FOREIGN KEY (version_id)
        REFERENCES pipeline_versions (id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pipeline_edges_version_id
    ON pipeline_edges(version_id);
