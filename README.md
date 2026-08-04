# Market Scout V2

An agentic content-generation workflow for a Nepali audience.  
This project focuses on trend spotting, script writing, structured outputs, image handling, and guardrails for reliable generation.

## Core Ideas

- **Explicit orchestration** — the loop is managed manually by calling the model, parsing the response, deciding the next action, and maintaining state across steps.
- **Token budget enforcement** — cumulative tokens are tracked per request/session and cut off before exceeding a ceiling.
- **Structured outputs** — JSON schema or `response_format` is used so outputs are parseable instead of requiring regex cleanup.
- **Problem-market fit** — the demo is targeted at one specific person’s specific pain point, supported by real problem discovery.

## Problem-Market Fit

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

## Next Improvements

- Add clearer schema examples for agent outputs.
- Document request and response flow in more detail.
- Add setup and run instructions.
- Include example inputs and sample outputs.