"""State passed through the prototype cognitive pipeline."""

from dataclasses import dataclass, field


@dataclass
class CognitiveState:
    """The information produced while processing one user request."""

    user_input: str
    purpose: str = ""
    response: str = ""
    notes: list[str] = field(default_factory=list)