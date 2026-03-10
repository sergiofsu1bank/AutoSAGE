from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    String,
    Float,
    Boolean,
    DateTime,
    UniqueConstraint,
    Text,
    ForeignKey,
    JSON,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from .base import Base


# ==================================================
# AGENTS
# ==================================================

class Agent(Base):
    __tablename__ = "agents"

    __table_args__ = (
        UniqueConstraint("name", name="uq_agents_name"),
    )

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    temperature: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    max_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    use_rag: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ==================================================
# DOCUMENT CHUNKS (RAG)
# ==================================================

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "agent_id",
            "content",
            name="uq_document_chunks_agent_content",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    agent_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1536),
        nullable=False,
    )

    chunk_metadata: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ==================================================
# PIPELINES
# ==================================================

class Pipeline(Base):
    __tablename__ = "pipelines"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ==================================================
# PIPELINE VERSION (versionamento futuro)
# ==================================================

class PipelineVersion(Base):
    __tablename__ = "pipeline_versions"

    __table_args__ = (
        UniqueConstraint(
            "pipeline_id",
            "version_number",
            name="uq_pipeline_version_number",
        ),
    )

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    pipeline_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("pipelines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ==================================================
# PIPELINE NODES
# ==================================================

from sqlalchemy import UniqueConstraint

class PipelineNode(Base):
    __tablename__ = "pipeline_nodes"

    __table_args__ = (
        UniqueConstraint(
            "version_id",
            "node_id",
            name="uq_pipeline_nodes_version_node",
        ),
    )

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    version_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("pipeline_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    node_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    agent_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

# ==================================================
# PIPELINE EDGES (DAG)
# ==================================================

class PipelineEdge(Base):
    __tablename__ = "pipeline_edges"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    version_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("pipeline_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_node_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    target_node_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    condition_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
