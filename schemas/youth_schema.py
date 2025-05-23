
from pydantic import BaseModel
from datetime import date, datetime


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
    pass

class YouthResponse(YouthBase):
    id: int

    class ConfigDict:
        from_attributes = True


    
