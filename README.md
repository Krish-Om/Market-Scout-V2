# Market Scout V2

An agentic content-generation workflow for a Nepali audience.  
This project focuses on trend spotting, script writing, structured outputs, image handling, and guardrails for reliable generation.

## Core Ideas

- **Explicit orchestration** — the loop is managed manually by calling the model, parsing the response, deciding the next action, and maintaining state across steps.
- **Token budget enforcement** — cumulative tokens are tracked per request/session and cut off before exceeding a ceiling.
- **Structured outputs** — JSON schema or `response_format` is used so outputs are parseable instead of requiring regex cleanup.
- **Problem-market fit** — the demo is targeted at one specific person’s specific pain point, supported by real problem discovery.

## 🧪 Idea Validation Plan

### 🎯 Core Hypothesis

Busy social media creators lack time to research viral TikTok trends and often post average content that struggles to perform.

### 👤 Target User

Creators who juggle content creation alongside other full-time work or primary responsibilities.

### 🔬 Validation Experiment (Concierge Test)

Before building the automated **Market-ScoutV2** pipeline:

1. **Manual Scout 📄**: Manually curate a 1-page "Weekly Trend Report" for a test group.
2. **Direct Outreach 🗣️**: Share the report with 5–10 target creators to test real interest.
3. **Success Metric 📈**: Creators actively apply the trend insights to their videos or request recurring reports.

### The Hook & Script Generator

- **Agent 1: Trend Analyzer**  
  Evaluates the clothing item and the target Nepali audience to brainstorm a viral hook.  
  Example: *“3 outfits under Rs. 2000 in Bhaktapur.”*

- **Agent 2: Script Writer**  
  Produces a structured JSON payload with:
  - audio script in Romanized Nepali/English
  - visual scene descriptions for filming

## Agents Flow

`trend_spotter → local_scriptwriter → guardrail → result`

If validation fails, the flow returns for a fix:

`trend_spotter → local_scriptwriter → guardrail → fix → local_scriptwriter`

## Project Notes and Logs

### July 30

Defined two agents:

- trend researcher / spotter
- scriptwriter for social media content creation

Prompts were generated with the help of Gemini and ChatGPT.

### July 31

Used the Groq SDK for agent orchestration.

### August 3

Moved toward image upload functionality and used the `llama-3-27b-verstaile` model.

### August 4

Converted uploaded images into encoded image bytes. Sending combined image bytes and prompt caused a token exceed error.

To address this:

- image and prompt were separated using SOC
- guardrails were added
- the workflow was shifted to textual processing only, since the free-tier API worked better with text than with encoded images

## Implementation Status

The following flow is working:

- agent orchestration
- structured content generation
- image upload handling
- guardrail validation
- fix-and-retry logic

## Repository Notes

The `app/` folder contains the main application logic:

- `config.py`
- `controller.py`
- `raw_orchestrator.py`
- `routes.py`
- `schemas.py`

## Questions

- Why might you choose to write your own orchestration instead of using an agent framework?
  We chose custom orchestration primarily for payload visibility and control. 🔍 Heavy frameworks abstract away the raw requests and responses, which makes debugging edge cases or JSON parsing errors really difficult. With hand-written orchestration, we have complete visibility into every prompt sent, exact API parameters, and raw responses, allowing us to log, debug, and optimize our pipeline with total precision.

- How do you guarantee a model's output matches a schema your downstream code depends on?
  To guarantee that a model's output strictly matches a required schema for downstream code 🛠️, production systems typically rely on three main strategies:

    Constrained Decoding (Engine/API Level) 🔒: Enforcing the schema directly during the model's sampling process using JSON Schema, GBNF grammars, or built-in API features (like OpenAI Structured Outputs or Outlines/vLLM). The model is physically prevented from generating tokens that break the schema.

    Schema Validation & Self-Correction (Application Level) 🔁: Passing raw output through a validator like Pydantic or Zod. If parsing fails, the exact error message is fed back into a second LLM call asking the model to fix its mistake.

    Structured Prompting & Few-Shot Examples (Prompt Level) 📝: Providing explicit schema definitions, field descriptions, and JSON examples directly in the system prompt to maximize first-pass success.

- How do you prevent an LLM retry loop from becoming a runaway-cost incident?
  The foundational safeguard is setting a hard MAX_RETRIES limit (typically 2–3 attempts per request) alongside exponential backoff. To further protect against runaway costs at scale, we combine this with fallback mechanisms (returning default safe responses on final failure), circuit breakers to pause calls during API outages, and API budget caps.

-

## Next Improvements

- Add clearer schema examples for agent outputs.
- Document request and response flow in more detail.
- Add setup and run instructions.
- Include example inputs and sample outputs