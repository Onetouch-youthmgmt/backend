from pydantic import BaseModel

class SabhaCenterBase(BaseModel):
    city: str
    address: str
    responsible_person: str
    contact_number: str
    name: str
class SabhaCenterCreate(SabhaCenterBase):
    pass

class SabhaCenterResponse(SabhaCenterBase):
    id: int
    
    class ConfigDict:
        from_attributes = True