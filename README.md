# Chowkidar — a watchman for your inbox

A multilingual scam message detector built for the WeMakeDevs × AWS Bharat Builds Tour hackathon (Build It track).

## The problem

Scam messages in India arrive in every language people actually text in — Hindi, Bengali, English, and mixes of all three. Most scam-detection tools only understand English, which leaves out exactly the people most often targeted: someone's parent, a grandparent, a first-time smartphone user more comfortable in their own language.

Chowkidar checks a suspicious message in the language it actually arrives in, and gives a plain-language explanation in that same language.

## How it works

Every message is checked by two independent systems:

1. **An AI agent** (Strands Agents SDK, running a local model via Ollama) reads the message and returns a structured verdict — is it a scam, how confident is it, what are the red flags, and a plain-language explanation in the message's own language.
2. **A rule-based policy engine**, inspired by AWS Cedar's policy-as-code approach, independently checks the message against known scam patterns (bank impersonation + urgency + callback demand, prize/lottery scams with links, OTP/PIN requests) using language-agnostic keyword extraction.

When both systems agree, the result is more trustworthy than either alone — this is shown directly in the UI as two separate verdicts side by side.

The app also tracks whether a message has been seen before, since scam texts are typically copy-pasted to thousands of people, and computes a combined 0–100 risk score from both systems' outputs.

## Tech stack

- **Backend**: FastAPI + SQLAlchemy (SQLite)
- **AI agent**: Strands Agents SDK, wrapping a local Ollama model (qwen2.5:7b)
- **Policy engine**: Custom Python rules engine, inspired by AWS Cedar's authorization-as-policy design
- **Frontend**: Vanilla HTML/CSS/JS, no framework — custom "stamped document" visual design
- **Serverless structure**: AWS SAM CLI, Lambda-shaped handler in `sam-app/`

## AWS tools used (Build It track)

- **Strands Agents SDK** — wraps the local language model into an agent
- **SAM CLI** — backend structured in Lambda-shaped format (`sam-app/scam_detector_function/`)
- **Cedar (concept)** — the policy engine follows Cedar's "rules over structured facts" design; implemented in plain Python (`policy.py`, `features.py`) after evaluating `cedarpy` directly, given time constraints
- **LocalStack** — evaluated for local AWS service simulation, but now requires account signup, which doesn't match the "no account, no card" premise stated for this track. Not used; documented here instead.
- **Finch** — attempted for container packaging; Linux release packaging wasn't straightforward to install in the time available. Left as a next step.

## Languages supported

Hindi (Devanagari script), Bengali (Bangla script), and English — validated on both scam and safe messages in each.

**Known limitation**: romanized/code-mixed text (e.g. "Aapka account block ho gaya") is not reliably supported by the current model and is out of scope for this submission.

**Future scope**: full 22-language rollout via [Bhashini](https://bhashini.gov.in), India's government language-translation infrastructure.

## Running it locally

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Pull the model (requires Ollama installed)
ollama pull qwen2.5:7b

# Run the server
uvicorn main:app --reload
\`\`\`

Then open http://127.0.0.1:8000

## What I learned

First time building an agent pipeline with Strands, and first time writing a deterministic policy layer alongside an LLM rather than relying on the model alone. Also learned the practical gap between "advertised open-source, no-account" tooling and what's actually frictionless to install under time pressure (LocalStack, Finch).
