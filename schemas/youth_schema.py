
from pydantic import BaseModel
from datetime import date, datetime

from schemas.sabha_center_schema import SabhaCenterResponse


class YouthBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    origin_city_india: str
    current_city_germany: str
    is_active: bool
    karyakarta_id: int
    educational_field: str
    created_at: datetime

class YouthCreate(YouthBase):
    sabha_center_ids: list[int]
    pass

class YouthResponse(YouthBase):
    id: int
    sabha_centers: list[SabhaCenterResponse]
    class ConfigDict:
        from_attributes = True


    
