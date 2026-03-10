from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os

from openai import OpenAI
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from src.db.session import SessionLocal
from src.db.models import DocumentChunk as DocumentChunkModel


# ==================================================
# Exceptions
# ==================================================

class RAGServiceError(Exception):
    pass


class RAGIngestionError(RAGServiceError):
    pass


class RAGRetrievalError(RAGServiceError):
    pass


# ==================================================
# Contracts
# ==================================================

@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    content: str
    source: str
    score: float
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class RAGQuery:
    query: str
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None


# ==================================================
# RAG Service
# ==================================================

class RAGService:
    """
    Database-backed RAG service using pgvector.
    """

    def __init__(self) -> None:
        self._openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # --------------------------------------------------
    # Embedding
    # --------------------------------------------------

    def generate_embedding(self, text: str) -> list[float]:
        response = self._openai.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding

    # --------------------------------------------------
    # Ingestion
    # --------------------------------------------------

    def ingest(
        self,
        *,
        agent_id: str,
        content: str,
        source: str,
    ) -> None:

        db = SessionLocal()

        try:
            embedding = self.generate_embedding(content)

            chunk = DocumentChunkModel(
                agent_id=agent_id,
                content=content,
                embedding=embedding,
                chunk_metadata={"source": source},
            )

            db.add(chunk)
            db.commit()

        except IntegrityError:
            db.rollback()
            print("Chunk duplicado ignorado.")

        finally:
            db.close()

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    def retrieve(
        self,
        *,
        agent_id: str,
        query: RAGQuery,
    ) -> list[DocumentChunk]:

        query_embedding = self.generate_embedding(query.query)

        db = SessionLocal()

        try:
            stmt = (
                select(DocumentChunkModel)
                .where(DocumentChunkModel.agent_id == agent_id)
                .order_by(
                    DocumentChunkModel.embedding.l2_distance(query_embedding)
                )
                .limit(query.top_k)
            )

            results = db.execute(stmt).scalars().all()

            print("RAG QUERY EMBEDDING GENERATED")
            print("AGENT ID:", agent_id)
            print("RESULTS COUNT:", len(results))

            print("DEBUG - rows retornadas:", len(results))

            chunks: list[DocumentChunk] = []

            for row in results:
                chunks.append(
                    DocumentChunk(
                        chunk_id=str(row.id),
                        content=row.content,
                        source=row.chunk_metadata.get("source") if row.chunk_metadata else "",
                        score=0.0,
                        metadata=row.chunk_metadata or {},
                    )
                )

            print("DEBUG - chunks convertidos:", len(chunks))

            return chunks

        finally:
            db.close()
