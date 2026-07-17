"""Constitutional supervision for the PCA prototype."""

from .state import CognitiveState


class Firekeeper:
    """Checks that the system informs rather than replaces human judgment."""

    def review(self, state: CognitiveState) -> None:
        state.agency_checks.append("Human decision authority is retained; this is a recommendation.")
        state.agency_checks.append("Alternatives and remaining uncertainty are communicated.")
        if not state.uncertainty:
            state.uncertainty.append("No external evidence has been independently verified.")
        if not state.hypotheses:
            state.critique.append("No alternatives were generated; do not treat this as a final decision.")