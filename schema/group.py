from pydantic import BaseModel
from typing import Optional

"""
Group: GET, PUT, POST, DELETE
"""
class GroupModel(BaseModel):
    group_id: str
    groupname: str
    organizer: str
    location: str
    category: str
    intro: str
    policy: str

class UpdateGroupModel(BaseModel):
    groupname: Optional[str] = None
    organizer: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    intro: Optional[str] = None
    policy: Optional[str] = None