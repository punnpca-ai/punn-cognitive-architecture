"""Constitutional supervision for the PCA prototype."""

from .state import CognitiveState

# Phrases that assert the decision for the user rather than support their own
# judgment. If the decision text uses this kind of coercive language, Firekeeper
# flags it instead of letting it pass silently.
COERCIVE_PHRASES = (
    "you must",
    "you have to",
    "you need to",
    "the only option",
    "there is no other way",
)

# Above this confidence, a claim needs corroborating memory to be trustworthy;
# without it, the number is unearned and should be flagged, not just displayed.
UNSUPPORTED_CONFIDENCE_THRESHOLD = 0.6


class Firekeeper:
    """Checks that the system informs rather than replaces human judgment."""

    def review(self, state: CognitiveState) -> None:
        state.agency_checks.append("Human decision authority is retained; this is a recommendation.")
        state.agency_checks.append("Alternatives and remaining uncertainty are communicated.")

        if not state.uncertainty:
            state.uncertainty.append("No external evidence has been independently verified.")

        if not state.hypotheses:
            state.critique.append("No alternatives were generated; do not treat this as a final decision.")

        decision_text = state.decision.lower()
        if any(phrase in decision_text for phrase in COERCIVE_PHRASES):
            state.critique.append(
                "Decision language asserts the choice rather than framing it as a recommendation; "
                "human agency may be undermined."
            )
            state.agency_checks.append("Coercive phrasing detected in decision text; flagged for review.")

        if state.confidence > UNSUPPORTED_CONFIDENCE_THRESHOLD and not state.memories:
            state.critique.append(
                f"Confidence ({state.confidence:.0%}) exceeds what unsupported evidence justifies; "
                "no corroborating memory was retrieved."
            )
            state.agency_checks.append("Confidence claim exceeds supporting evidence; flagged for review.")