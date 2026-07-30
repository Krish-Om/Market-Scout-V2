## 📋 Section 3: Data Contracts & Data Validation Schemas

This section defines the data structures for **Market-Scout-V2** using Pydantic. These schemas serve two purposes: they act as internal state objects between agents, and they serve as public-facing data contracts for API clients.

---

### 3.1 Data Schema Interfacing

To maximize pipeline reliability and reduce runtime failures, our system separates its data contracts into two discrete phases:

```
[Vision Input + Search Lookups] ──>  ProductAnalysis (Internal)
                                              │
                                     [Synthesis Loop]
                                              ▼
Client Interface                <─── MarketingPayloadResponse (Public)

```

1. **Internal Domain Models:** Ingest raw, messy outputs from unstructured external tasks (like multi-modal image evaluation and HTML web scraping) and parse them into strongly-typed objects.
2. **Public Presentation Models:** Flatten complex, nested text generations into explicit, predictable API contracts that a frontend dashboard can safely map directly to user interface panels without performing string manipulation.

---

### 3.2 Pydantic Data Contract Implementation (`schemas.py`)

Below is the complete, production-grade schema architecture implementing explicit field constraints and data-typing:

```python
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# 1. INTERNAL AGENT DATA COMPONENT SCHEMAS
# ==========================================

class ScriptScene(BaseModel):
    """Defines the structural blueprint for a single scene in a social video storyboard."""
    visual_direction: str = Field(
        ..., 
        description="Detailed camera framing, movement, lighting, or action cues for the frame."
    )
    voiceover: str = Field(
        ..., 
        description="The spoken narration script, voiceover audio track, or verbal dialogue."
    )
    on_screen_text: str = Field(
        ..., 
        description="Text overlays, titles, captions, or typography graphical elements rendered on the video."
    )

class VideoScript(BaseModel):
    """Provides a sequential, step-by-step layout structured specifically for short-form video formats."""
    hook: ScriptScene = Field(
        ..., 
        description="The opening scene (first 3 seconds) engineered to optimize user hook-rate and retain attention."
    )
    body: List[ScriptScene] = Field(
        ..., 
        description="A list of sequential scenes demonstrating product features, utility, or aesthetic design details."
    )
    call_to_action: ScriptScene = Field(
        ..., 
        description="The final scene prompting users toward a measurable conversion goal."
    )

class ProductAnalysis(BaseModel):
    """
    The unified internal context state. Captures raw multi-modal image tags and coordinates 
    them alongside dynamic, external search engine lookup summaries.
    """
    dominant_colors: List[str] = Field(
        ..., 
        description="Extracted key color identifiers or descriptive names from the uploaded image payload."
    )
    vibe: str = Field(
        ..., 
        description="The overall style vertical, subculture, or cultural aesthetic alignment (e.g., minimalist streetwear)."
    )
    design_details: List[str] = Field(
        ..., 
        description="Explicit physical markers identified in the image, such as fabric weave, textures, pocket styles, or fit profiles."
    )
    market_trends: List[str] = Field(
        ..., 
        description="Dynamic keyword search trends and high-volume consumer interest phrases pulled from the web."
    )
    season: str = Field(
        ..., 
        description="The calculated primary retail target season based on current timeline data and trend queries."
    )
    price_range: str = Field(
        ..., 
        description="The evaluated marketplace target index determined via real-time competitor benchmarking."
    )


# ==========================================
# 2. PUBLIC USER OUTBOUND INTERFACE SCHEMAS
# ==========================================

class MarketingPayloadResponse(BaseModel):
    """
    The deterministic public data contract returned to the client interface. 
    Guarantees structural consistency for direct UI binding.
    """
    social_media_posts: List[str] = Field(
        ..., 
        description="Fully formatted long-form ad copy optimized for multi-platform distribution."
    )
    captions: List[str] = Field(
        ..., 
        description="Short text variations designed for captions or micro-blogging formats."
    )
    hooks: List[str] = Field(
        ..., 
        description="Alternative text variations focused entirely on primary opening hooks for marketing split-tests."
    )
    cta: str = Field(
        ..., 
        description="The primary action directive aimed at driving immediate user conversion."
    )
    video_script: VideoScript = Field(
        ..., 
        description="A highly structured video script layout parsed cleanly into distinct visual, verbal, and textual nodes."
    )

```