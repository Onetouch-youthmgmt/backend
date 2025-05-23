from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.database import Base
from sqlalchemy.orm import relationship
class Karyakarta(Base):
    __tablename__ = "karyakartas"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String)

    # Youth managed by user/karyakarta
    managed_youths = relationship("Youth", back_populates="karyakarta")

    def __repr__(self):
        return f"Karyakarta( email={self.email} )"
