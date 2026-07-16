"""Purpose-identification stage for the PCA prototype."""

from .state import CognitiveState


class PurposeEngine:
    """Establish a transparent, human-centred purpose before generation."""

    def process(self, state: CognitiveState) -> CognitiveState:
        """Record the purpose for the current request and return its state."""
        request = state.user_input.strip()
        if request:
            state.purpose = (
                "Help the user understand and make an informed decision about: "
                f"{request}"
            )
        else:
            state.purpose = "Ask the user for a question before generating a response."

        return state