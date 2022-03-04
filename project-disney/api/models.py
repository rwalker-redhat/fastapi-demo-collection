from sqlalchemy import Column, Integer, String, Date
from api.database import Base


class CartoonCharacter(Base):
    __tablename__ = "cartoon_characters"

    id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String)
    first_appearance = Column(Date)
    first_appearance_title = Column(String)
    species = Column(String)
    gender = Column(String)

