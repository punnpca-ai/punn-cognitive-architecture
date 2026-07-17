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
        sources = {item["source"] for item in later.memories}
        self.assertIn("cognitive_dna_cycle", sources)
        layers = {item["layer"] for item in later.memories}
        self.assertIn(MemoryLayer.REFLECTIVE.value, layers)
        self.assertIn(MemoryLayer.WORKING.value, layers)

    def test_memory_retains_provenance(self):
        memory = MemoryEngine()
        memory.remember(MemoryItem("Evidence supports review", MemoryLayer.SEMANTIC, "test", 0.9))

        result = memory.retrieve("review evidence")

        self.assertEqual("test", result[0].source)
        self.assertEqual(MemoryLayer.SEMANTIC, result[0].layer)

    def test_purpose_stage_uses_purpose_engine_not_duplicated_logic(self):
        state = Orchestrator(use_llm=False).think("Should I take the job offer?")

        purpose_output = state.trace[2]["output"]
        self.assertEqual("purpose", state.trace[2]["stage"])
        self.assertIn("Should I take the job offer?", purpose_output["purpose"])
        self.assertIn("human-owned decision", purpose_output["purpose"])
        self.assertTrue(purpose_output["constraints"])

    def test_current_observation_does_not_self_match_its_own_retrieval(self):
        memory = MemoryEngine()
        orchestrator = Orchestrator(memory=memory, use_llm=False)

        state = orchestrator.think("Plan the research budget")

        self.assertEqual([], state.memories)

    def test_confidence_reflects_memory_reliability_not_a_flat_constant(self):
        memory = MemoryEngine()
        memory.remember(MemoryItem("budget plan evidence", MemoryLayer.SEMANTIC, "test", 0.9))
        orchestrator = Orchestrator(memory=memory, use_llm=False)

        state = orchestrator.think("budget plan evidence review")

        # baseline (0.3, observation present) + 0.9 * 0.5 memory component = 0.75
        self.assertAlmostEqual(state.confidence, 0.75, places=2)

    def test_firekeeper_flags_coercive_decision_language(self):
        orchestrator = Orchestrator(use_llm=False)
        state = orchestrator.think("Plan a project")
        state.decision = "You must do this immediately, there is no other way."

        orchestrator.firekeeper.review(state)

        self.assertTrue(any("Coercive phrasing" in note for note in state.agency_checks))

    def test_firekeeper_flags_unsupported_high_confidence(self):
        orchestrator = Orchestrator(use_llm=False)
        state = orchestrator.think("Plan a project")
        state.confidence = 0.9
        state.memories = []

        orchestrator.firekeeper.review(state)

        self.assertTrue(any("exceeds what unsupported evidence justifies" in note for note in state.critique))

    def test_thai_input_gets_thai_deterministic_fallback(self):
        state = Orchestrator(use_llm=False).think("ควรตัดสินใจอย่างไรดี")

        self.assertEqual("th", state.language)
        self.assertIn("การตัดสินใจสุดท้ายยังคงเป็นของคุณ", state.response)

    def test_english_input_still_gets_english_fallback(self):
        state = Orchestrator(use_llm=False).think("How should I decide?")

        self.assertEqual("en", state.language)
        self.assertIn("You retain the final decision", state.response)

    def test_requirements_only_lists_used_dependencies(self):
        from pathlib import Path

        requirements = Path(__file__).resolve().parents[1] / "prototype" / "requirements.txt"
        content = requirements.read_text().split()

        self.assertEqual(["requests"], content)


if __name__ == "__main__":
    unittest.main()