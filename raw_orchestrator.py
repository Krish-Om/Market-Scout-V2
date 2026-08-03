# Problem Market Fit:
"""
The "Bhaktapur Backdrop" Concept Generator 🎬

    Agent 1 (Trend Spotter): Takes a basic clothing item she wants to sell (e.g., "Pastel Kurti set" or "Casual summer dress") and pairs it with a trending TikTok audio style or challenge concept.

    Agent 2 (Local Scriptwriter): Formats a precise JSON payload detailing the exact visual shot list (e.g., Shot 1: Walking past the standard wood-carved windows in Sakotha), the on-screen text overlays, and the Romanized Nepali voiceover script.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# Agents Schema
class Agent:
    role: str
    content: str

    def __init__(self, role, content):
        self.role = role
        self.content = content


trend_spotter_agent_prompt = """You are a Hyper-Local TikTok Fashion Trend Spotter for Bhaktapur. Analyze the text description of the clothing item and context, then output ONE executable, high-conversion TikTok concept optimized for smartphone production.

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
trend_spotter_agent = Agent(
    role="system",
    content=trend_spotter_agent_prompt,
)


local_scriptwriter_prompt = """
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


async def start_trend_spotter_agent(cloth_description):
    system_instruction = trend_spotter_agent.content

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_instruction,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze the following clothing image and generate a TikTok concept: {cloth_description}",
                        },
                    ],
                },
            ],
            temperature=0.2,
            reasoning_format="hidden",
            # max_tokens=1024,
        )
        trend_spotter_response = response.choices[0].message.content
        return trend_spotter_response
    except Exception as e:
        print(f"Error in trend spotter agent: {e}")
        raise


async def start_local_scriptwriter_agent(trend_spotter_response):
    local_scriptwriter_response = (
        client.chat.completions.create(
            model="openai/gpt-oss-20b",
            # response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": local_scriptwriter_prompt,
                },
                {
                    "role": "user",
                    "content": str(trend_spotter_response),
                },
            ],
        )
        .choices[0]
        .message.content
    )
    return local_scriptwriter_response


async def process_image_and_generate_script(cloth_description="Pastel Kurti set with floral embroidery, perfect for summer outings.") -> str:
    try:
        trend_spotter_response = await start_trend_spotter_agent(cloth_description)
        local_scriptwriter_response = await start_local_scriptwriter_agent(
            trend_spotter_response
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    return (
        local_scriptwriter_response
        or "No response generated from the local scriptwriter agent."
    )


# if __name__ == "__main__":
#     import asyncio

#     async def main():
#         print("Processing and generating script...")
#         result = await process_image_and_generate_script(
#             cloth_description
#         )
#         with open("generated_tiktok_script.json", "w") as f:
#             f.write(result)

#     asyncio.run(main())
