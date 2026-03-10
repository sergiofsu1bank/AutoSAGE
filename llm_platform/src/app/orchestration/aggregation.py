from pydantic import BaseModel
from typing import List


class AggregationDefinition(BaseModel):
    """
    Define como múltiplos outputs são combinados.
    """
    aggregation_type: str  # merge | list | forward | custom
    input_keys: List[str]
    output_key: str
