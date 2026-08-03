import uuid

from fastapi import UploadFile
from pydantic import BaseModel
from typing import List


class UserInput(BaseModel):
    def __init__(self, user_input: str):
        """Describe the clothes in plain english. For example, "A stylish summer dress with floral patterns, perfect for a casual day out in Bhaktapur."""
        self.user_input = user_input

    __table_name__ = "user_input"
    # id: uuid.UUID
    user_input: str


class UserOutput(BaseModel):
    result : dict
    pass


# Agents Schema
class Agent:
    role: str
    content: str

    def __init__(self, role, content):
        self.role = role
        self.content = content
