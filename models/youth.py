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
    is_karyakarta = Column(Boolean, default=False)


    ## FK to the Karyakarta
    karyakarta_id = Column(Integer, ForeignKey('youths.id'), nullable=True)
    karyakarta = relationship("Youth", remote_side=[id], back_populates="managed_youths")

    # youth managed by KK
    managed_youths = relationship("Youth", back_populates="karyakarta", cascade="all, delete-orphan")   

    ## mtom relationship with sabha_center
    sabha_centers=relationship("SabhaCenter", secondary="youth_sabha_center_association", back_populates="youths")
    

    # relationship with attendances
    youth_attendances = relationship("Attendance", back_populates="youth")

    def __repr__(self):
        return f"Youth( last_name={self.last_name}, email={self.email},first_name={self.first_name} )"