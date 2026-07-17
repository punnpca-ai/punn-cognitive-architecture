"""Executable PCA Cognitive DNA prototype with optional Ollama communication."""

import re

from .core.cognitive_dna import COGNITIVE_DNA, CognitiveStage
from .core.governance import Firekeeper
from .core.memory import MemoryEngine, MemoryItem, MemoryLayer
from .core.state import CognitiveState
from .llm.ollama import OllamaClient, OllamaUnavailable


class Orchestrator:
    """Coordinates the invariant Cognitive DNA sequence without hidden reasoning."""

    def __init__(
        self,
        memory: MemoryEngine | None = None,
        llm: OllamaClient | None = None,
        use_llm: bool = True,
    ) -> None:
        self.memory = memory or MemoryEngine()
        self.firekeeper = Firekeeper()
        self.llm = llm or OllamaClient()
        self.use_llm = use_llm

    def start(self) -> None:
        mode = f"Ollama model: {self.llm.model}" if self.use_llm else "deterministic fallback"
        print(f"PCA Cognitive DNA prototype initialized ({mode}).")

    def think(self, user_input: str) -> CognitiveState:
        state = CognitiveState(user_input=user_input)
        self._observe(state)
        self._understand(state)
        self._identify_purpose(state)
        self._retrieve_memory(state)
        self._build_mental_model(state)
        self._generate_hypotheses(state)
        self._evaluate_evidence(state)
        self._critique(state)
        self.firekeeper.review(state)
        self._decide(state)
        self._communicate(state)
        self._reflect(state)
        self._learn(state)
        self._validate_trace(state)
        return state

    def _observe(self, state: CognitiveState) -> None:
        observation = state.user_input.strip()
        if observation:
            state.observations.append(observation)
        else:
            state.uncertainty.append("No request was provided.")
        state.record(CognitiveStage.OBSERVATION, {"observations": state.observations, "uncertainty": state.uncertainty[:]})

    def _understand(self, state: CognitiveState) -> None:
        state.understanding = "The user is seeking support to examine a request before acting."
        if not state.observations:
            state.understanding = "There is insufficient input to establish context."
        state.record(CognitiveStage.UNDERSTANDING, {"understanding": state.understanding})

    def _identify_purpose(self, state: CognitiveState) -> None:
        state.purpose = "Strengthen the user's understanding and support an informed, human-owned decision."
        state.constraints = ["Do not replace human judgment.", "State uncertainty explicitly.", "Prefer evidence over assumption."]
        state.record(CognitiveStage.PURPOSE, {"purpose": state.purpose, "constraints": state.constraints})

    def _retrieve_memory(self, state: CognitiveState) -> None:
        retrieved = self.memory.retrieve(state.user_input)
        state.memories = [item.as_dict() for item in retrieved]
        state.record(CognitiveStage.MEMORY, {"retrieved": state.memories})

    def _build_mental_model(self, state: CognitiveState) -> None:
        state.mental_models = ["A good response distinguishes observed input, alternatives, evidence, and a user-owned choice."]
        state.record(CognitiveStage.MENTAL_MODEL, {"models": state.mental_models})

    def _generate_hypotheses(self, state: CognitiveState) -> None:
        if state.observations:
            state.hypotheses = [
                {"claim": "Clarifying the desired outcome will improve the next action.", "status": "candidate"},
                {"claim": "Relevant prior context may change the recommended action.", "status": "candidate"},
            ]
        state.record(CognitiveStage.HYPOTHESIS, {"hypotheses": state.hypotheses})

    def _evaluate_evidence(self, state: CognitiveState) -> None:
        evidence_count = len(state.observations) + len(state.memories)
        state.confidence = min(0.8, 0.25 + evidence_count * 0.15) if evidence_count else 0.0
        for hypothesis in state.hypotheses:
            hypothesis["confidence"] = round(state.confidence, 2)
        if not state.memories:
            state.uncertainty.append("No relevant prior memory was available.")
        state.record(CognitiveStage.EVIDENCE_EVALUATION, {"confidence": state.confidence, "ranked_hypotheses": state.hypotheses, "uncertainty": state.uncertainty[:]})

    def _critique(self, state: CognitiveState) -> None:
        state.critique.append("The input alone is not independent evidence; verify important claims before acting.")
        if len(re.findall(r"[a-zA-Z0-9']+", state.user_input)) < 4:
            state.critique.append("The request is brief; ask for context before making a high-impact choice.")
        state.record(CognitiveStage.CRITIQUE, {"critique": state.critique[:]})

    def _decide(self, state: CognitiveState) -> None:
        if not state.observations:
            state.decision = "Ask the user to provide a specific question or goal."
        else:
            state.decision = "Clarify the desired outcome, compare available alternatives, and let the user choose the next action."
        state.record(CognitiveStage.DECISION, {"decision": state.decision, "confidence": state.confidence, "uncertainty": state.uncertainty[:]})

    def _communication_prompt(self, state: CognitiveState) -> str:
        return f"""You are the Communication stage of the PUNN Cognitive Architecture (PCA).\nRespond in the user's language. Help them think; do not make their decision for them.\nSeparate observations from assumptions, state uncertainty, and offer practical options.\n\nUser request: {state.user_input}\nPurpose: {state.purpose}\nDecision framework: {state.decision}\nConfidence: {state.confidence:.0%}\nUncertainty: {'; '.join(state.uncertainty)}\nCritique: {'; '.join(state.critique)}\n\nGive a concise, helpful response."""

    def _fallback_response(self, state: CognitiveState) -> str:
        return "\n".join([
            f"Understanding: {state.understanding}",
            f"Purpose: {state.purpose}",
            f"Recommendation: {state.decision}",
            f"Confidence: {state.confidence:.0%}",
            "Uncertainty: " + "; ".join(state.uncertainty),
            "Agency: You retain the final decision.",
        ])

    def _communicate(self, state: CognitiveState) -> None:
        source = "deterministic_fallback"
        if self.use_llm:
            try:
                state.response = self.llm.chat(self._communication_prompt(state))
                source = "ollama"
            except OllamaUnavailable as exc:
                state.notes.append(str(exc))
        if not state.response:
            state.response = self._fallback_response(state)
        state.record(CognitiveStage.COMMUNICATION, {"response": state.response, "source": source})

    def _reflect(self, state: CognitiveState) -> None:
        state.reflection.append("The cycle preserved observations separately from hypotheses and communicated uncertainty.")
        state.record(CognitiveStage.REFLECTION, {"reflection": state.reflection[:]})

    def _learn(self, state: CognitiveState) -> None:
        if state.observations:
            item = MemoryItem(content=state.observations[0], layer=MemoryLayer.REFLECTIVE, source="cognitive_dna_cycle", confidence=state.confidence, context={"purpose": state.purpose})
            self.memory.remember(item)
            state.learning.append("Stored a traceable reflective memory for future relevance-based retrieval.")
        state.record(CognitiveStage.LEARNING, {"learning": state.learning[:]})

    def _validate_trace(self, state: CognitiveState) -> None:
        observed = tuple(entry["stage"] for entry in state.trace)
        expected = tuple(stage.value for stage in COGNITIVE_DNA)
        if observed != expected:
            raise RuntimeError("Cognitive DNA stages must execute once and in specification order.")