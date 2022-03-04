from sqlalchemy import Column, Boolean, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    characters = relationship("CartoonCharacter", back_populates="owner")


class CartoonCharacter(Base):
    __tablename__ = "cartoon_characters"

    id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String)
    first_appearance = Column(Date)
    first_appearance_title = Column(String)
    species = Column(String)
    gender = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="characters")
