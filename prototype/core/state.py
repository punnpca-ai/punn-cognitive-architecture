"""State passed through one complete PCA Cognitive DNA cycle."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .cognitive_dna import CognitiveStage


@dataclass
class CognitiveState:
    """Inspectable state shared by every cognitive stage."""

    user_input: str
    purpose: str = ""
    response: str = ""
    notes: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    understanding: str = ""
    constraints: list[str] = field(default_factory=list)
    memories: list[dict[str, Any]] = field(default_factory=list)
    mental_models: list[str] = field(default_factory=list)
    hypotheses: list[dict[str, Any]] = field(default_factory=list)
    decision: str = ""
    confidence: float = 0.0
    uncertainty: list[str] = field(default_factory=list)
    critique: list[str] = field(default_factory=list)
    reflection: list[str] = field(default_factory=list)
    learning: list[str] = field(default_factory=list)
    agency_checks: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)

    def record(self, stage: CognitiveStage, output: dict[str, Any]) -> None:
        """Record transparent, timestamped output from one cognitive stage."""
        self.trace.append(
            {
                "stage": stage.value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "output": output,
            }
        )