from datetime import  datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Date, Integer, Table
from database.database import Base
from sqlalchemy.orm import relationship
from models.attendance import Attendance
from models.sabha_center import SabhaCenter

youth_sabha_center_association = Table(
    "youth_sabha_center_association",
    Base.metadata,
    Column("youth_id", Integer, ForeignKey("youths.id")),
    Column("sabha_center_id", Integer, ForeignKey("sabha_centers.id")),
)

class Youth(Base):
    __tablename__ = "youths"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String,unique=True, nullable=False)
    origin_city_india = Column(String, nullable=False)
    current_city_germany = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    educational_field = Column(String, nullable=True)


    ## FK to the Karyakarta
    karyakarta_id = Column(Integer, ForeignKey('karyakartas.id'), nullable=True)
    karyakarta = relationship("Karyakarta", back_populates="managed_youths")

    ## mtom relationship with sabha_center
    sabha_centers=relationship("SabhaCenter", secondary="youth_sabha_center_association", back_populates="youths")
    

    # relationship with attendances
    youth_attendances = relationship("Attendance", back_populates="youth")

    def __repr__(self):
        return f"Youth( last_name={self.last_name}, email={self.email},first_name={self.first_name} )"