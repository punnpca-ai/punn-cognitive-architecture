"""Architectural regression tests for the PCA Cognitive DNA prototype."""

import unittest

from prototype.core.cognitive_dna import COGNITIVE_DNA
from prototype.core.memory import MemoryEngine, MemoryItem, MemoryLayer
from prototype.llm.ollama import OllamaUnavailable
from prototype.orchestrator import Orchestrator


class FakeOllama:
    model = "fake-model"

    def chat(self, prompt: str) -> str:
        self.prompt = prompt
        return "A model-supported response"


class UnavailableOllama:
    model = "offline-model"

    def chat(self, prompt: str) -> str:
        raise OllamaUnavailable("offline")


class CognitiveDnaTests(unittest.TestCase):
    def test_executes_every_stage_in_specification_order(self):
        state = Orchestrator(use_llm=False).think("How should I decide between two options?")

        self.assertEqual([stage.value for stage in COGNITIVE_DNA], [entry["stage"] for entry in state.trace])
        self.assertTrue(state.response)

    def test_communication_preserves_agency_and_uncertainty(self):
        state = Orchestrator(use_llm=False).think("Plan a project")

        self.assertIn("You retain the final decision", state.response)
        self.assertTrue(state.uncertainty)
        self.assertTrue(state.agency_checks)

    def test_ollama_communication_uses_cognitive_context(self):
        llm = FakeOllama()
        state = Orchestrator(llm=llm).think("Help me plan a trip")

        self.assertEqual("A model-supported response", state.response)
        self.assertIn("human-owned decision", llm.prompt)
        self.assertEqual("ollama", state.trace[9]["output"]["source"])

    def test_unavailable_ollama_falls_back_without_breaking_the_cycle(self):
        state = Orchestrator(llm=UnavailableOllama()).think("Plan a project")

        self.assertIn("You retain the final decision", state.response)
        self.assertIn("offline", state.notes[0])

    def test_learning_makes_a_traceable_memory_available_to_a_later_cycle(self):
        memory = MemoryEngine()
        orchestrator = Orchestrator(memory=memory, use_llm=False)
        orchestrator.think("Improve the research plan")
        later = orchestrator.think("Research plan evidence")

        self.assertTrue(later.memories)
        self.assertEqual("cognitive_dna_cycle", later.memories[0]["source"])

    def test_memory_retains_provenance(self):
        memory = MemoryEngine()
        memory.remember(MemoryItem("Evidence supports review", MemoryLayer.SEMANTIC, "test", 0.9))

        result = memory.retrieve("review evidence")

        self.assertEqual("test", result[0].source)
        self.assertEqual(MemoryLayer.SEMANTIC, result[0].layer)


if __name__ == "__main__":
    unittest.main()