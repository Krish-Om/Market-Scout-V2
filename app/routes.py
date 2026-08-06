from fastapi import APIRouter, HTTPException
from app.controller import start_pipeline
from app.schemas import ClothingDescription, ContextNotes, FinalScript

router = APIRouter(prefix="/v1/generation", tags=["generation"])


@router.post("/generation", response_model=FinalScript, status_code=200)
async def generate_script(
    clothing_description: ClothingDescription, context_notes: ContextNotes
):
    """
    Endpoint to upload a clothing description and context notes, and receive a verified script.
    """
    try:
        # Call the run_tiktok_pipeline function with the provided inputs
        verified_script = await start_pipeline(
            clothing_description.description, context_notes.notes
        )
        return {"status": "PASSED", "verified_script": verified_script}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Error: {str(e)}")


@router.get("/health", status_code=200)
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "API is running"}
