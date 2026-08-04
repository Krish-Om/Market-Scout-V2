from fastapi import APIRouter, HTTPException, UploadFile, File
from models import UserInput, UserOutput

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/upload", response_model=UserOutput,status_code=200)
async def upload_file(user_input: UserInput):
    """_summary_
    Routing to Handle Single Image Only.

    Args:
        user_input (UserInput): _description_

    Returns:
        _type_: UserOutput

    """
    # Process the uploaded file and description here
    try:
        image_file = await user_input.image.read()
        # Pass it to the controller or service layer for further processing
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Failed to read the uploaded file.")

    # For example, you can save the file or perform some analysis
    return UserOutput()  # Return an appropriate response