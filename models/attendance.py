from sqlalchemy import Column, ForeignKey, Boolean, Integer, UniqueConstraint
from database.database import Base
from sqlalchemy.orm import relationship

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True)

    # FK to the Sabha
    sabha_id = Column(Integer, ForeignKey('sabhas.id'), nullable=False)
    sabha = relationship("Sabha", back_populates="sabha_attendances")

    # FK to the Youth
    youth_id = Column(Integer, ForeignKey('youths.id'), nullable=True)
    youth = relationship("Youth", back_populates="youth_attendances")

    is_present = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint('sabha_id', 'youth_id', name='uix_sabha_youth'),
    )
    

    def __repr__(self):
        return f"Attendance(sabha_id={self.id} )"
    
    
