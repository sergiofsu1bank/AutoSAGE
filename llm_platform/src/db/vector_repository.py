from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.db.models import DocumentChunk


class VectorRepository:

    def __init__(self, db: Session) -> None:
        self.db = db

    def insert_chunk(
        self,
        *,
        agent_id: str,
        content: str,
        embedding: list[float],
        chunk_metadata: dict | None = None,
    ) -> DocumentChunk:

        chunk = DocumentChunk(
            agent_id=agent_id,
            content=content,
            embedding=embedding,
            chunk_metadata=chunk_metadata,
        )

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk

    def similarity_search(
        self,
        *,
        agent_id: str,
        query_embedding: list[float],
        k: int = 5,
    ) -> List[DocumentChunk]:

        stmt = text("""
            SELECT *
            FROM document_chunks
            WHERE agent_id = :agent_id
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :k
        """)

        result = self.db.execute(
            stmt,
            {
                "agent_id": agent_id,
                "query_embedding": query_embedding,
                "k": k,
            },
        )

        rows = result.mappings().all()

        return [
            DocumentChunk(**row)
            for row in rows
        ]
