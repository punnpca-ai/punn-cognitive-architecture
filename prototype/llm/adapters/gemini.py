import os
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from .base import BaseLLMAdapter

class GeminiAdapter(BaseLLMAdapter):
    def __init__(
        self,
        model: str = "gemini-pro",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> None:
        super().__init__(model=model, temperature=temperature, **kwargs)
        genai.configure(api_key=api_key or os.getenv("GEMINI_API_KEY"))

    def generate(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "parts": [prompt]}]
        return self.chat(messages, **kwargs)

    def chat(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        try:
            model_instance = genai.GenerativeModel(self.model)
            # Gemini API expects messages in a specific format for chat
            # This is a simplified conversion; a more robust solution might be needed
            # depending on the exact message structure from the orchestrator.
            gemini_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    gemini_messages.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    gemini_messages.append({"role": "model", "parts": [msg["content"]]})

            response = model_instance.generate_content(
                gemini_messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    **kwargs
                )
            )
            return response.text.strip()
        except Exception as exc:
            raise RuntimeError(f"Gemini API error: {exc}") from exc
