from pydantic import BaseModel


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