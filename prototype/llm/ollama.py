import requests


class OllamaClient:

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "qwen3:4b",
    ):
        self.host = host
        self.model = model

    def chat(self, prompt: str) -> str:

        url = f"{self.host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(url, json=payload)

        response.raise_for_status()

        data = response.json()

        return data["response"]
