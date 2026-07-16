"""Regression tests for the runnable PCA prototype."""

import unittest
from unittest.mock import Mock

from prototype.core.purpose import PurposeEngine
from prototype.core.state import CognitiveState
from prototype.orchestrator import Orchestrator


class PurposeEngineTests(unittest.TestCase):
    def test_process_sets_a_purpose_for_a_request(self):
        state = PurposeEngine().process(CognitiveState(user_input="How should I plan this?"))

        self.assertIn("How should I plan this?", state.purpose)

    def test_process_handles_empty_requests(self):
        state = PurposeEngine().process(CognitiveState(user_input="   "))

        self.assertIn("Ask the user", state.purpose)


class OrchestratorTests(unittest.TestCase):
    def test_think_returns_a_completed_cognitive_state(self):
        orchestrator = Orchestrator()
        orchestrator.llm = Mock()
        orchestrator.llm.chat.return_value = "A considered response"

        state = orchestrator.think("Help me decide")

        self.assertEqual("Help me decide", state.user_input)
        self.assertIn("Help me decide", state.purpose)
        self.assertEqual("A considered response", state.response)
        orchestrator.llm.chat.assert_called_once_with("Help me decide")


if __name__ == "__main__":
    unittest.main()