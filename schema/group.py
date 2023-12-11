from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict

"""
Resource Model for response 
"""
class GroupModel(BaseModel):
    group_id: str
    groupname: str
    organizer: str
    location: str
    category: str
    intro: str
    policy: str

class GroupFullModel(BaseModel):
    group_id: str
    groupname: str
    organizer: str
    location: str
    category: str
    intro: str
    policy: str
    records: Dict[str, HttpUrl]
    events: Dict[str, HttpUrl]

class UpdateGroupModel(BaseModel):
    groupname: Optional[str] = None
    organizer: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    intro: Optional[str] = None
    policy: Optional[str] = None