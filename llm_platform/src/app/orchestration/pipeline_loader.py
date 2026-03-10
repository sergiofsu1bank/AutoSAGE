from typing import Optional, Dict, List

from src.db.session import SessionLocal
from src.db.pipeline_repository import PipelineRepository

from src.app.orchestration.contracts import (
    PipelineDefinition,
    PipelineNode,
    PipelineEdge,
    Condition,
)


class PipelineLoader:
    """
    Responsável por:
    - Carregar pipeline ativo do banco
    - Transformar em PipelineDefinition (modelo de execução)
    """

    def __init__(self, trace_id: str) -> None:
        self._db = SessionLocal()
        self._repo = PipelineRepository(self._db, trace_id)

    def load(self, pipeline_name: str) -> Optional[PipelineDefinition]:
        """
        Retorna PipelineDefinition pronto para engine.
        """

        data = self._repo.load_full_pipeline_structure(pipeline_name)

        if not data:
            return None

        version = data["version"]
        nodes_model = data["nodes"]
        edges_model = data["edges"]

        # ==============================
        # Nodes
        # ==============================

        nodes: Dict[str, PipelineNode] = {}

        for node in nodes_model:
            nodes[node.node_id] = PipelineNode(
                node_id=node.node_id,
                agent_id=node.agent_id,
            )

        # ==============================
        # Edges
        # ==============================

        edges: List[PipelineEdge] = []

        for edge in edges_model:
            condition = None

            if edge.condition_json:
                condition = Condition(
                    type=edge.condition_json.get("type"),
                    expression=edge.condition_json.get("expression"),
                )

            edges.append(
                PipelineEdge(
                    source=edge.source_node_id,
                    target=edge.target_node_id,
                    condition=condition,
                )
            )

        # ==============================
        # Detectar Start Nodes
        # ==============================

        all_targets = {e.target for e in edges}
        start_nodes = [
            node_id
            for node_id in nodes.keys()
            if node_id not in all_targets
        ]

        # ==============================
        # Detectar End Nodes
        # ==============================

        all_sources = {e.source for e in edges}
        end_nodes = [
            node_id
            for node_id in nodes.keys()
            if node_id not in all_sources
        ]

        self._db.close()

        return PipelineDefinition(
            nodes=nodes,
            edges=edges,
            start_nodes=start_nodes,
            end_nodes=end_nodes,
        )
