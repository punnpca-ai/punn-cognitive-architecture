"""Invariant Cognitive DNA stage definitions."""

from enum import Enum


class CognitiveStage(str, Enum):
    OBSERVATION = "observation"
    UNDERSTANDING = "understanding"
    PURPOSE = "purpose"
    MEMORY = "memory"
    MENTAL_MODEL = "mental_model"
    HYPOTHESIS = "hypothesis"
    EVIDENCE_EVALUATION = "evidence_evaluation"
    CRITIQUE = "critique"
    DECISION = "decision"
    COMMUNICATION = "communication"
    REFLECTION = "reflection"
    LEARNING = "learning"


COGNITIVE_DNA = tuple(CognitiveStage)
