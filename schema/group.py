from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict

"""
Resource Model for response 
"""
class GroupModel(BaseModel):
    group_id: str
    group_name: str
    founder: str
    location: str
    category: str
    intro: str
    policy: str


class UpdateGroupModel(BaseModel):
    group_name: Optional[str] = None
    founder: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    intro: Optional[str] = None
    policy: Optional[str] = None


class GroupMemberModel(BaseModel):
    group_id: str
    username: str