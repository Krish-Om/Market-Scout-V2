
from fastapi import UploadFile
from raw_orchestrator import client, start_local_scriptwriter_agent, start_trend_spotter_agent

async def process_and_generate_script(cloth_description: str) -> str:
    """ Process User Input and Extract the cloth description from it.

    Args:
        cloth_description (str): _description_

    Returns:
        str: _description_
    """
    try:
        trend_spotter_response = await start_trend_spotter_agent(cloth_description)
        local_scriptwriter_response = await start_local_scriptwriter_agent(
            trend_spotter_response
        )   
        return local_scriptwriter_response
    except Exception as e:
        print(f"Error in processing and generating script: {e}")
        raise