from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseLLMAdapter(ABC):
    """Abstract base class for all LLM adapters."""

    def __init__(self, model: str, temperature: float = 0.7, **kwargs):
        self.model = model
        self.temperature = temperature

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generates a response from the LLM based on the given prompt."""
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generates a chat response from the LLM based on the given messages."""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(model=\"{self.model}\")"