from pydantic import BaseModel
from typing import Optional

"""
Resource Model for response 
"""
class RecordModel(BaseModel):
    record_id: str
    group_id: str
    content: str
    publisher: int

class UpdateRecordModel(BaseModel):
    record_id: Optional[str] = None
    content: Optional[str] = None
    publisher: Optional[int] = None