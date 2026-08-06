from pydantic import BaseModel, Field


class ClothingDescription(BaseModel):
    description: str = Field(
        ..., description="A detailed description of the clothing item.",
        examples=["Traditional Newari black cotton sari with red border."],
    )


class ContextNotes(BaseModel):
    notes: str = Field(
        ...,
        description="Additional context or notes related to the clothing item.",
        examples=["Worn during golden hour in Bhaktapur."]
    )


class FinalScript(BaseModel):
    status: str = Field(
        ...,
        description="The status of the script verification (e.g., PASSED or FAILED).",
        examples=["PASSED","FAILED"]
    )
    verified_script: dict = Field(
        ..., description="The final verified script output from the pipeline."
    )
