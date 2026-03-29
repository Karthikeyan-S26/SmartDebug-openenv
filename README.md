---
title: SmartDebug Env
emoji: 📊
colorFrom: pink
colorTo: green
sdk: docker
pinned: false
---

# SmartDebug: Recursive Debugger OpenEnv

SmartDebug is an OpenEnv-based environment designed for training AI agents to debug code interactively. It operates on a recursive step-based loop, allowing agents to edit syntax, run tests, and observe outcomes dynamically until successful execution is achieved.

## Features

- **Step-Based Debugging**: Agents can iteratively edit lines of code and execute tests in a controlled feedback loop.
- **Progressive Difficulty Levels**: Includes built-in debugging tasks categorized as easy, medium, and hard.
- **RESTful API Endpoints**: Fully accessible via FastAPI with distinct endpoints tailored for state querying, environment resets, and action steps.
- **Docker Deployment**: Pre-configured Dockerfile ensuring secure execution and cross-platform compatibility.

## Environment Design

The framework strictly enforces a reinforcement learning-style architecture to interface with AI models:

- **Observation**: Retains the complete string representation of the active code, alongside previous test results and diagnostic error logs.
- **Action**: Accepts a structured JSON payload dictating an `action_type` (e.g., `edit_line` or `run_tests`), a target `line_number`, and the `new_code`.
- **Reward**: Uses a deterministic scoring system evaluating `passed_tests / total_tests`, scaling from `0.0` to `1.0`.

## Example Debugging Flow

1. **Buggy Code State**: The environment initializes with an intentional logic flaw.
```python
def add(a, b):
    return a - b  # bug
```

2. **Action (Edit)**: The agent issues a JSON request to modify the erroneous line.
```json
{
  "action_type": "edit_line",
  "line_number": 2,
  "new_code": "    return a + b"
}
```

3. **Action (Test)**: The agent triggers the testing suite to validate the new logic.
```json
{
  "action_type": "run_tests"
}
```

4. **Success Outcome**: The tests validate successfully, computing a perfect score and returning the `done: true` flag.

## Deterministic Behavior

SmartDebug evaluates code in an isolated standard execution context via `grader.py`. It guarantees perfectly reproducible and stateless scoring results by systematically separating evaluation logic. Scores strictly correlate with deterministic validation on predefined static test parameters, computing exactly to the bounded `0.0` to `1.0` scale on every iteration.

## Real-World Impact

This environment bridges the gap between isolated programmatic text generation and fully autonomous agentic coding. By training AI logic within this bounded environment, models learn to systematically synthesize test results, backtrack logical mistakes, and verify syntax identically to a human engineer.

## Local Setup

Ensure you have Python 3.9+ installed and run the following in your terminal to initialize the API:

```bash
pip install fastapi uvicorn "pydantic<2.10"
uvicorn server.app:app --reload
```
You can verify the API locally by visiting `http://localhost:8000/docs`.

## Docker Instructions

The repository includes a production-ready container environment configured to enforce unprivileged UID mapping suitable for standard execution contexts.

```bash
# Build the container locally
docker build -t smartdebug-env .

# Run the container mapping to internal port 7860
docker run -d -p 7860:7860 --name sd-tmp smartdebug-env
```
Access the Dockerized environment locally at `http://localhost:7860/docs`.

## Deployment

SmartDebug is entirely configured for immediate web hosting and is seamlessly deployed on **Hugging Face Spaces**. Utilizing the included front-matter YAML configuration metadata, Hugging Face automatically parses the required Docker SDK framework and executes the API within its serverless Space engine.
