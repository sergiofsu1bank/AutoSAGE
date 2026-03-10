from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func

from src.db.models import (
    Pipeline,
    PipelineVersion,
    PipelineNode,
    PipelineEdge,
)


class PipelineRepository:
    """
    Repository responsável por:
    - Criar pipelines
    - Gerenciar versionamento
    - Persistir nós e edges
    - Carregar estrutura completa
    """

    def __init__(self, db: Session, trace_id: str) -> None:
        self.db = db
        self.trace_id = trace_id

    # ==================================================
    # Pipeline
    # ==================================================

    def create_pipeline(self, name: str) -> Pipeline:
        pipeline = Pipeline(name=name)
        self.db.add(pipeline)
        self.db.commit()
        self.db.refresh(pipeline)
        return pipeline

    def get_pipeline_by_name(self, name: str) -> Optional[Pipeline]:
        stmt = select(Pipeline).where(Pipeline.name == name)
        return self.db.execute(stmt).scalar_one_or_none()

    # ==================================================
    # Versionamento
    # ==================================================

    def _get_next_version_number(self, pipeline_id: str) -> int:
        stmt = (
            select(func.max(PipelineVersion.version_number))
            .where(PipelineVersion.pipeline_id == pipeline_id)
        )

        result = self.db.execute(stmt).scalar_one_or_none()

        if result is None:
            return 1

        return result + 1

    def create_new_version(
        self,
        *,
        pipeline_id: str,
        activate: bool = True,
    ) -> PipelineVersion:
        """
        Cria nova versão incremental.
        Se activate=True → desativa versões anteriores.
        """

        next_version = self._get_next_version_number(pipeline_id)

        if activate:
            stmt = (
                update(PipelineVersion)
                .where(PipelineVersion.pipeline_id == pipeline_id)
                .values(is_active=False)
            )
            self.db.execute(stmt)

        version = PipelineVersion(
            pipeline_id=pipeline_id,
            version_number=next_version,
            is_active=activate,
        )

        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)

        return version

    def get_active_version(
        self,
        pipeline_id: str,
    ) -> Optional[PipelineVersion]:

        stmt = (
            select(PipelineVersion)
            .where(PipelineVersion.pipeline_id == pipeline_id)
            .where(PipelineVersion.is_active == True)
        )

        return self.db.execute(stmt).scalar_one_or_none()

    # ==================================================
    # Nodes
    # ==================================================

    def add_node(
        self,
        *,
        pipeline_version_id: str,
        node_id: str,
        agent_id: str,
    ) -> PipelineNode:

        node = PipelineNode(
            version_id=pipeline_version_id,
            node_id=node_id,
            agent_id=agent_id,
        )

        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)

        return node

    def list_nodes(
        self,
        pipeline_version_id: str,
    ) -> List[PipelineNode]:

        stmt = select(PipelineNode).where(
            PipelineNode.version_id == pipeline_version_id
        )

        return self.db.execute(stmt).scalars().all()

    # ==================================================
    # Edges
    # ==================================================

    def add_edge(
        self,
        *,
        version_id: str,
        source_node_id: str,
        target_node_id: str,
        condition_json: dict | None = None,
    ):

        edge = PipelineEdge(
            version_id=version_id,
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            condition_json=condition_json,
        )

        self.db.add(edge)
        self.db.commit()

    def list_edges(self, version_id: str):
        return (
            self.db.query(PipelineEdge)
            .filter(
                PipelineEdge.version_id == version_id
            )
            .all()
        )

    # ==================================================
    # Loader Helper
    # ==================================================

    def load_full_pipeline_structure(
        self,
        pipeline_name: str,
    ) -> Optional[dict]:
        """
        Retorna estrutura completa:

        {
            "pipeline": Pipeline,
            "version": PipelineVersion,
            "nodes": [...],
            "edges": [...]
        }
        """

        pipeline = self.get_pipeline_by_name(pipeline_name)
        if not pipeline:
            return None

        version = self.get_active_version(pipeline.id)
        if not version:
            return None

        nodes = self.list_nodes(version.id)
        edges = self.list_edges(version.id)

        return {
            "pipeline": pipeline,
            "version": version,
            "nodes": nodes,
            "edges": edges,
        }
