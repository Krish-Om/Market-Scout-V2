from fastapi import HTTPException

from app.raw_orchestrator import run_tiktok_pipeline

async def start_pipeline(clothing_description: str, context_notes: str = "") -> dict:
    """
    Initiates the TikTok script generation pipeline.
    
    Args:
        clothing_description (str): A detailed description of the clothing item.
        context_notes (str): Additional context or notes related to the clothing item.
        
    Returns:
        dict: The final verified script output from the pipeline.
    """
    try:
        verified_script = await run_tiktok_pipeline(clothing_description, context_notes)
        return verified_script
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     