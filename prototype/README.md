# PCA Cognitive DNA Prototype

A deterministic, inspectable reference prototype for **PCA Specification v1.0 (Draft)**.

## What it demonstrates

- The complete Cognitive DNA lifecycle in specification order: Observation, Understanding, Purpose, Memory, Mental Model, Hypothesis, Evidence Evaluation, Critique, Decision, Communication, Reflection, and Learning.
- Transparent, timestamped stage outputs held in a shared `CognitiveState`.
- Traceable multi-layer memory with source, context, timestamp, and confidence.
- Firekeeper supervision that preserves Human Agency and surfaces uncertainty.
- Deterministic behaviour with no model or network dependency.

This is an educational partial reference implementation, not a claim of full PCA compliance.

## Run

From the repository root:

```bash
python -m prototype.app
```

## Test

```bash
python -m unittest discover -s tests -v
```
## Ollama

The CLI uses the local `qwen3:4b` model through Ollama for the Communication stage. Keep Ollama running, then start the app as above. If Ollama is unavailable, the prototype continues with its transparent deterministic fallback and reports the reason as a system note.

The session remains open for follow-up questions. Type `exit` or `quit` to close it.