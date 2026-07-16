from llm.ollama import OllamaClient


class Orchestrator:

    def __init__(self):
        self.llm = OllamaClient()

    def start(self):
        print("Orchestrator initialized.")

    def think(self, prompt: str):

        return self.llm.chat(prompt)
