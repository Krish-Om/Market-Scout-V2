# • Explicit orchestration — you now write the loop yourself: call the model, parse the response, decide the next action, manage state across steps.

# • Token budget enforcement — track cumulative tokens per request/session and cut off before a ceiling, logging every call.

# • Structured outputs — use JSON schema / response_format so the model returns a parseable shape instead of free text you regex out of.

# • Problem-market fit — skill inventory, problem identification, real user interviews, and a demo targeted at one specific person's specific pain.

# Problem Market Fit:

The Hook & Script Generator 🎬:

    Agent 1 (Trend Analyzer): Evaluates the clothing item and the target Nepali audience to brainstorm a viral "hook" (e.g., "3 outfits under Rs. 2000 in Bhaktapur").

    Agent 2 (Script Writer): Outputs a structured JSON payload containing the exact audio script (in Romanized Nepali/English) and visual scene descriptions for her to film.
