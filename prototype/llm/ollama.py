"""Ollama integration with bounded failures for the PCA prototype."""

import requests


class OllamaUnavailable(RuntimeError):
    """Raised when a local Ollama model cannot provide a response."""


class OllamaClient:
    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "qwen3:4b",
        timeout: float = 60.0,
    ) -> None:
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json().get("response", "").strip()
        except (requests.RequestException, ValueError) as exc:
            raise OllamaUnavailable(f"Ollama is unavailable: {exc}") from exc

        if not content:
            raise OllamaUnavailable("Ollama returned an empty response.")
        return content