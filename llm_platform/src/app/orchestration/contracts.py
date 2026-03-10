from pydantic import BaseModel, Field, model_validator
from typing import Dict, List, Optional, Any


class Condition(BaseModel):
    """
    Condição declarativa avaliada pela Execution Engine.
    """
    type: str = Field(..., description="Tipo da condição. Ex: 'expression'")
    expression: str = Field(..., min_length=1, description="Expressão booleana declarativa")

    @model_validator(mode="after")
    def validate_type(self):
        if self.type != "expression":
            raise ValueError("Only condition type 'expression' is supported")
        return self


class PipelineNode(BaseModel):
    """
    Um nó do DAG.
    Representa a execução de um agente ou agregação.
    """
    node_id: str = Field(..., min_length=1)
    agent_id: Optional[str] = None
    aggregation_type: Optional[str] = None
    input_keys: Optional[List[str]] = None
    output_key: Optional[str] = None

    @model_validator(mode="after")
    def validate_node_type(self):
        if not self.agent_id and not self.aggregation_type:
            raise ValueError(
                "PipelineNode must define either agent_id or aggregation_type"
            )

        if self.agent_id and self.aggregation_type:
            raise ValueError(
                "PipelineNode cannot define both agent_id and aggregation_type"
            )

        return self

class PipelineEdge(BaseModel):
    """
    Transição entre nós do pipeline.
    Pode conter condição declarativa.
    """
    source: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)
    condition: Optional[Condition] = None


class PipelineDefinition(BaseModel):
    """
    Pipeline declarativo (DAG).
    """
    nodes: Dict[str, PipelineNode]
    edges: List[PipelineEdge]
    start_nodes: List[str]
    end_nodes: List[str]
    execution_metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_pipeline(self):
        for node_id in self.start_nodes:
            if node_id not in self.nodes:
                raise ValueError(f"start_node '{node_id}' not found in nodes")

        for node_id in self.end_nodes:
            if node_id not in self.nodes:
                raise ValueError(f"end_node '{node_id}' not found in nodes")

        return self
