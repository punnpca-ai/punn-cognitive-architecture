from config import APP_NAME, VERSION
from orchestrator import Orchestrator


def main():

    print("=" * 40)
    print(APP_NAME)
    print(f"Version: {VERSION}")
    print("=" * 40)

    orchestrator = Orchestrator()

    orchestrator.start()

    print()

    question = input("You: ")

    state = orchestrator.think(question)

    print()

    print("Purpose")
    print(state.purpose)

    print()

    print("PCA")
    print(state.response)

    print()

    print("=" * 40)


if __name__ == "__main__":
    main()