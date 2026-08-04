# • Explicit orchestration — you now write the loop yourself: call the model, parse the response, decide the next action, manage state across steps.

# • Token budget enforcement — track cumulative tokens per request/session and cut off before a ceiling, logging every call.

# • Structured outputs — use JSON schema / response_format so the model returns a parseable shape instead of free text you regex out of.

# • Problem-market fit — skill inventory, problem identification, real user interviews, and a demo targeted at one specific person's specific pain.

# Problem Market Fit:

The Hook & Script Generator 🎬:

    Agent 1 (Trend Analyzer): Evaluates the clothing item and the target Nepali audience to brainstorm a viral "hook" (e.g., "3 outfits under Rs. 2000 in Bhaktapur").

    Agent 2 (Script Writer): Outputs a structured JSON payload containing the exact audio script (in Romanized Nepali/English) and visual scene descriptions for her to film.

July 30
Defined two agents , trend researcher or spotter and scriptwriter, social media content creator agent.
Generated their respective prompts with the help of Gemini and ChatGPT.

july31
Using GROQ SDK for agent orchestration.

Aug 3:
Going with Image upload functionality.
Using the llama-3-27b-verstaile model.

Aug4:
Converting the Uploaded image into a encoded image bytes.
Sending combined bytes image and prompt to the agent, which led to TokenExceed Error
So, using SOC, separating both image and prompt separately.
Using guardrails.

## Agents Flow

trend_spotter ➔ local_scriptwriter ➔ guardrail ──(Passed)──> result
                      ^                     │
                      └────(Failed: Fix)────┘
Successfully implemented the logic of above flow
