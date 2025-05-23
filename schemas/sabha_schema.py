from pydantic import BaseModel
from datetime import date

class SabhaBase(BaseModel):
    topic: str
    speaker_name: str
    date: date
    sabha_center_id: int
class SabhaCreate(SabhaBase):
    pass

class SabhaResponse(SabhaBase):
    id: int
    
