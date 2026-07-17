import requests
from typing import Any, Dict, List

from .base import BaseLLMAdapter

class OllamaUnavailable(RuntimeError):
    """Raised when a local Ollama model cannot provide a response."""

class OllamaAdapter(BaseLLMAdapter):
    def __init__(
        self,
        model: str = "qwen3:4b",
        host: str = "http://localhost:11434",
        temperature: float = 0.7,
        timeout: float = 60.0,
        **kwargs
    ) -> None:
        super().__init__(model=model, temperature=temperature, **kwargs)
        self.host = host.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # Ollama's /api/generate endpoint expects a single prompt string,
        # so we'll concatenate messages for simplicity in this adapter.
        # For a more robust solution, consider using /api/chat endpoint if available
        # or a more sophisticated prompt templating.
        full_prompt = "\n".join([f"{msg["role"]}: {msg["content"]}" for msg in messages])

        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": self.temperature}
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json().get("response", "").strip()
        except (requests.RequestException, ValueError) as exc:
            raise OllamaUnavailable(f"Ollama is unavailable: {exc}") from exc

        if not content:
            raise OllamaUnavailable("Ollama returned an empty response.")
        return content