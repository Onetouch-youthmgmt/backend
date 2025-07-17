
from typing import Optional
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
    educational_field: str
    created_at: datetime
    is_karyakarta: bool
    karyakarta_id: Optional[int]=None
    address: Optional[str] = None
    pin_code: Optional[str] = None


class YouthCreate(YouthBase):
    sabha_center_ids: list[int]

class YouthResponse(YouthBase):
    id: int
    sabha_centers: list[SabhaCenterResponse]
    karyakarta_name: Optional[str] = None
    class ConfigDict:
        from_attributes = True

class YouthKaryakartaResponse(BaseModel):
    id: int
    name: str
    created_date: datetime

    class ConfigDict:
        from_attributes = True


    
