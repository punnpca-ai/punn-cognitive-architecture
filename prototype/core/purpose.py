"""Purpose-identification stage for the PCA prototype."""

from .state import CognitiveState


DEFAULT_CONSTRAINTS = [
    "Do not replace human judgment.",
    "State uncertainty explicitly.",
    "Prefer evidence over assumption.",
]


class PurposeEngine:
    """Establish a transparent, human-centred purpose before generation."""

    def process(self, state: CognitiveState) -> CognitiveState:
        """Record the purpose and constraints for the current request."""
        request = state.user_input.strip()
        if state.language == "th":
            if request:
                state.purpose = f"ช่วยให้ผู้ใช้เข้าใจและตัดสินใจได้เอง (human-owned decision) เกี่ยวกับ: {request}"
            else:
                state.purpose = "ขอให้ผู้ใช้ระบุคำถามก่อนที่จะสร้างคำตอบ"
        else:
            if request:
                state.purpose = (
                    "Help the user understand and make an informed, human-owned decision about: "
                    f"{request}"
                )
            else:
                state.purpose = "Ask the user for a question before generating a response."

        state.constraints = list(DEFAULT_CONSTRAINTS)
        return state