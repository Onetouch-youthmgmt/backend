from pydantic import BaseModel

class KaryakartaCreateSchema(BaseModel):
    email: str
    hashed_password: str
    role: str
