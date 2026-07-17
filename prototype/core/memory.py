"""Traceable multi-layer memory for the PCA prototype."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import re


class MemoryLayer(str, Enum):
    WORKING = "working"
    SESSION = "session"
    PROJECT = "project"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    REFLECTIVE = "reflective"


@dataclass
class MemoryItem:
    content: str
    layer: MemoryLayer
    source: str
    confidence: float = 0.5
    context: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, object]:
        return {
            "content": self.content,
            "layer": self.layer.value,
            "source": self.source,
            "confidence": self.confidence,
            "context": self.context,
            "created_at": self.created_at,
        }


class MemoryEngine:
    """Retains traceable information and retrieves it by lexical relevance."""

    def __init__(self) -> None:
        self._items: list[MemoryItem] = []

    def remember(self, item: MemoryItem) -> None:
        self._items.append(item)

    def retrieve(self, query: str, limit: int = 5) -> list[MemoryItem]:
        terms = set(re.findall(r"[a-zA-Z0-9']+", query.lower()))
        ranked = []
        for item in self._items:
            item_terms = set(re.findall(r"[a-zA-Z0-9']+", item.content.lower()))
            score = len(terms & item_terms) * item.confidence
            if score:
                ranked.append((score, item))
        return [item for _, item in sorted(ranked, key=lambda pair: pair[0], reverse=True)[:limit]]