from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentContent:
    text: str
    source_id: str
    project_id: str
    source_name: str
    source_type: str
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)