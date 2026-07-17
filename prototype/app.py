"""Command-line application for the PCA Cognitive DNA prototype."""

import sys

from .config import APP_NAME, VERSION
from .orchestrator import Orchestrator


def main() -> None:
    # Local models may return emoji that legacy Windows code pages cannot encode.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    print("=" * 60)
    print(APP_NAME)
    print(f"Version: {VERSION}")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 60)

    orchestrator = Orchestrator()
    orchestrator.start()

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        if question.lower() in {"exit", "quit"}:
            print("Session ended.")
            break
        if not question:
            print("Please enter a question or type 'exit'.")
            continue

        state = orchestrator.think(question)
        print()
        print(state.response)
        print()
        print("Cognitive DNA trace:")
        print(" -> ".join(entry["stage"] for entry in state.trace))
        if state.notes:
            print("System note:", state.notes[-1])


if __name__ == "__main__":
    main()