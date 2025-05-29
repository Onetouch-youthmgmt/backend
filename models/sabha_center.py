
from sqlalchemy import  Column, String, Integer
from database.database import Base
from sqlalchemy.orm import relationship


class SabhaCenter(Base):
    __tablename__ = "sabha_centers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    responsible_person = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)

    # relationship with sabhas
    sabhas = relationship("Sabha", back_populates="sabha_center")

    ## relationship with sabha youth
    youths=relationship("Youth", secondary="youth_sabha_center_association", back_populates="sabha_centers")

    def __repr__(self):
        return f"<SabhaCenter id={self.id} city={self.city})>"