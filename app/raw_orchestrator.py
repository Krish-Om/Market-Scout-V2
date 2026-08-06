import json
import os
from groq import Groq
from dotenv import load_dotenv
from app.config import Config
from app.utils import track_tokens

load_dotenv()  # Load environment variables from .env file

# 🔑 Initialize Client
if not Config.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")
client = Groq(api_key=Config.GROQ_API_KEY)

# 📜 Agent Prompts
TREND_SPOTTER_PROMPT = """You are a Hyper-Local TikTok Fashion Trend Spotter for Bhaktapur. Analyze the text description of the clothing item and context, then output ONE executable, high-conversion TikTok concept optimized for smartphone production.

Priority:
1) Make the garment the visual hero using Bhaktapur architecture (brick, carved wood, stone) as purposeful storytelling.
2) Deliver a scroll-stopping hook within 0–3s.
3) Maximize immediate conversion: visit shop and/or DM on Instagram.
4) Keep production realistic, low-budget, and culturally respectful to Newari heritage.

Output (strict structure):
[Visual Insights]
- Clothing Visual DNA: dominant colors, fabric, silhouette, visible details based on the description.
- Best Bhaktapur Pairing: specific location type and why (visual contrast or harmony).
- Visual Strategy: framing, light, color contrast to make the item pop.

[The Hook]
- Concept: TikTok format (e.g., POV, transition, reveal).
- First 0–3s: exact visual camera action, framing, and actor movement.
- On-screen text / Voiceover: exact lines (short, punchy).
- Why it stops the scroll: 1–2 short reasons.

[Vibe & Sequence]
- Overall vibe: mood, tempo, edit style.
- Shot list: 5–8 numbered shots (shot type, duration, purpose).
- Transition idea: describe the cut or match move.
- Audio direction: music style and suggested sound cues.

[Conversion]
- Primary CTA: exact final overlay text.
- Recommend action: Visit Shop / DM on Instagram / Both.
- Conversion mechanism: how the CTA is delivered.

[One-line Summary]
- Single actionable sentence for the creator.

Only use facts provided in the text description; do not invent hidden details. Keep answers concise and production-ready.
local_scriptwriter = Agent(role="system", content=local_scriptwriter_prompt)


"""

SCRIPTWRITER_PROMPT = """
AGENT 2: LOCAL TIKTOK SCRIPTWRITER & PRODUCER — Bhaktapur

Role: Turn Agent 1's creative concept into a compact, production-ready TikTok script with timing, camera directions, exact on-screen text, and Romanized Nepali lines. The script must be executable with a smartphone, minimal crew, and real Bhaktapur locations.

Inputs you'll receive:
- Trend Spotter output (structured sections: Visual Insights, The Hook, Vibe & Sequence, Conversion)
- Optional contextual notes (shop name, Instagram handle, pricing, offers)

Rules:
1) Preserve Agent 1's core idea. Make only execution-level edits for clarity, timing, or feasibility.
2) Never invent or change confirmed visual facts from the text description.
3) Keep language simple, natural, and localized (Romanized Nepali for voice lines).
4) Do not add unsupported fabric characteristics or accessories that change the look.

Required output:
Return your response inside a valid JSON object matching the schema below. Do not wrap the JSON in markdown code blocks (such as ```json). Do not add any text, explanations, or comments before or after the JSON object.

{
  "meta_info": {
    "chosen_format": "string",
    "total_estimated_duration": "number (in seconds)",
    "overall_vibe_description": "string"
  },
  "audio_direction": {
    "sound_type": "string",
    "audio_timing_strategy": "string",
    "sfx_cues": ["string"]
  },
  "script_timeline": [
    {
      "shot_number": "number",
      "timestamp": "string (e.g., 0:00-0:02)",
      "location": "string",
      "camera_framing": "string",
      "camera_action": "string",
      "subject_action": "string",
      "visual_description": "string",
      "on_screen_text": "string or null",
      "voiceover_script": "string or null",
      "audio_cue": "string or null"
    }
  ],
  "conversion_ending": {
    "final_cta_text": "string",
    "recommended_action_type": "string",
    "production_note": "string"
  }
}
"""

GUARDRAIL_PROMPT = """
ROLE: SYSTEM QA & GUARDRAIL VALIDATOR (Bhaktapur TikTok Pipeline)

CRITICAL INSTRUCTION: You MUST respond ONLY in valid JSON format. Do not include markdown code blocks (```json), intro text, or trailing comments.
OBJECTIVE:
You are the final safety, cultural, and technical check. Review the generated outputs from Agent 1 (Trend Spotter) and Agent 2 (Scriptwriter) against the input constraints. Flag any violations or output a clean "PASSED".

CHECKLIST:

1. FACT & IMAGE GROUNDING (Anti-Hallucination)
- Verify that no visual details are invented beyond what was provided in the image metadata/description.
- Ensure no fake business details are invented (e.g., fake addresses, prices, phone numbers, or Instagram handles). Missing details must be represented as `null` or placeholder.

2. CULTURAL RESPECT & LOCAL ACCURACY
- Check that Bhaktapur heritage (Newari architecture, brick, carved wood, local atmosphere) is treated respectfully as an active story element, not generic tourism wallpaper.
- Verify that Romanized Nepali voiceover lines sound natural, respectful, and appropriate for local short-form content.

3. FORMAT & SCHEMA COMPLIANCE
- Ensure Agent 2's output is STRICTLY valid, parseable JSON with no markdown formatting (no ```json code blocks), no leading text, and no trailing commas.
- Verify shot timestamps are chronological, non-overlapping, and total 12–20 seconds (5–8 shots).

4. CONVERSION & COMMERCIAL ALIGNMENT
- Confirm the Call-To-Action (CTA) clearly directs the viewer to a specific action (Visit Shop, DM on Instagram, or Both).

OUTPUT FORMAT:
If ANY check fails:
Return JSON:
{
  "status": "FAILED",
  "reasons": ["Specific description of failure 1", "Specific description of failure 2"],
  "suggested_fixes": ["Actionable correction for Agent 1 or 2"]
}

If ALL checks pass:
Return JSON:
{
  "status": "PASSED",
  "verified_script": {
  "title":"String", 
  "shots":[]
  }
} """


@track_tokens
async def call_llm(system_prompt: str, user_input: str, json_mode: bool = False) -> str:
    """Helper function to execute a completion call using the Groq SDK."""
    kwargs = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        "max_tokens": 2048,
        "temperature": 0.2,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response


async def run_tiktok_pipeline(
    clothing_description: str, context_notes: str = ""
) -> dict:
    from app.utils import run_metrics

    run_metrics.clear()
    """Orchestrates Trend Spotter -> Scriptwriter -> Guardrail Loop."""
    # 📊 Step 1: Agent 1 (Trend Spotter)
    print("📊 Generating trend concept...")
    trend_input = (
        f"Clothing Description: {clothing_description}\nContext: {context_notes}"
    )
    trend_output = await call_llm(TREND_SPOTTER_PROMPT, trend_input)

    # 🔄 Steps 2 & 3: Agent 2 & Guardrail Loop
    MAX_RETRIES = 3
    current_input = (
        f"Trend Spotter Concept:\n{trend_output}\nContext Notes: {context_notes}"
    )

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"✍️ Running Scriptwriter (Attempt {attempt}/{MAX_RETRIES})...")
        script_output = await call_llm(
            SCRIPTWRITER_PROMPT, current_input, json_mode=True
        )

        print("🛡️ Running Guardrail QA Check...")
        guardrail_raw = await call_llm(GUARDRAIL_PROMPT, script_output, json_mode=True)
        guardrail_result = json.loads(guardrail_raw)

        if guardrail_result.get("status") == "PASSED":
            print("✅ Script passed all guardrail checks!")
            total_tokens = sum(
                item["prompt_tokens"] + item["completion_tokens"]
                for item in run_metrics
            )
            total_cost = sum(item["cost_usd"] for item in run_metrics)
            return {
                "script": guardrail_result.get("verified_script"),
                "metrics": {"total_tokens": total_tokens, "total_cost_usd": total_cost},
            }

        # ⚠️ Failed validation: collect reasons and prepare retry prompt
        reasons = guardrail_result.get("reasons", [])
        fixes = guardrail_result.get("suggested_fixes", [])
        print(f"⚠️ Guardrail Failed: {reasons}")

        current_input = (
            f"PREVIOUS SCRIPT FAILED VALIDATION.\n"
            f"Reasons: {reasons}\n"
            f"Fix Instructions: {fixes}\n"
            f"Original Trend Concept:\n{trend_output}"
        )

    # 🚨 Raise error if max retries exceeded
    raise RuntimeError(
        f"Pipeline execution failed after {MAX_RETRIES} attempts.\n"
        f"Last Guardrail Feedback: {guardrail_result}"
    )


# Define your input inputs
# clothing_desc = "Pastel Kurti set with floral embroidery, perfect for summer outings."
# context_info = "Shop: Fashion Island | IG: @fashionisland | Price: NPR 3,500"

# # Execute the multi-agent pipeline
# try:
#     final_script = run_tiktok_pipeline(clothing_desc, context_info)
#     print("🎉 Pipeline Execution Complete! Here is your script:\n")
#     print(json.dumps(final_script, indent=2))
#     with open("final_script.json", "w") as f:
#         json.dump(final_script, f, indent=2)
# except Exception as e:
#     print(f"❌ Execution failed: {e}")
