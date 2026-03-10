-- Extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop seguro
DROP TABLE document_chunks CASCADE;

-- Criação da tabela
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    chunk_metadata JSONB,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Índice para filtro por agente
CREATE INDEX idx_document_chunks_agent_id
ON document_chunks(agent_id);

-- Índice vetorial (cosine distance)
CREATE INDEX idx_document_chunks_embedding
ON document_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Recomendado após criar IVFFLAT
ANALYZE document_chunks;
