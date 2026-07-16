from core.state import CognitiveState
from core.purpose import PurposeEngine
from llm.ollama import OllamaClient


class Orchestrator:

    def __init__(self):
        self.purpose = PurposeEngine()
        self.llm = OllamaClient()

    def start(self):
        print("Orchestrator initialized.")

    def think(self, user_input: str) -> CognitiveState:

        # Create cognitive state
        state = CognitiveState(user_input=user_input)

        # Stage 1: Purpose
        state = self.purpose.process(state)

        # LLM Response (temporary for Prototype v0.1)
        state.response = self.llm.chat(state.user_input)

        return state