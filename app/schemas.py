from pydantic import BaseModel, Field

class ClothingDescription(BaseModel):
    description: str = Field(..., description="A detailed description of the clothing item.")

class ContextNotes(BaseModel):
    notes: str = Field(..., description="Additional context or notes related to the clothing item.")


class FinalScript(BaseModel):
    status: str = Field(..., description="The status of the script verification (e.g., PASSED or FAILED).")
    verified_script: dict = Field(..., description="The final verified script output from the pipeline.")