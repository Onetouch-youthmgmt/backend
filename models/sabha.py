from sqlalchemy import  Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from database.database import Base
from models.attendance import Attendance
class Sabha(Base):
    __tablename__ = "sabhas"

    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    speaker_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    # FK sabha_center_id
    sabha_center_id = Column(Integer, ForeignKey('sabha_centers.id'), nullable=False)
    sabha_center = relationship("SabhaCenter", back_populates="sabhas")

    # relationship with attendances
    sabha_attendances = relationship("Attendance", back_populates="sabha")


    def __repr__(self):
        return f"<Sabha topic={self.topic})>"
    
    