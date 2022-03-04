from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from api import models
from api.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, Field
from datetime import date

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Character(BaseModel):
    character_name: str = Field(min_length=1)
    first_appearance: date = Field(default='2000-01-01')
    first_appearance_title: Optional[str] = Field(title="First cartoon character appeared in",
                                                  max_length=100,
                                                  min_length=1,
                                                  default=None)
    species: Optional[str] = Field(min_length=1, max_length=100)
    gender: str = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "character_name": "Peter Pan",
                "first_appearance": "1902-12-01",
                "first_appearance_title": "The Little White Bird",
                "species": "Boy",
                "gender": "Male"
            }
        }


# Read
@router.get("/api/")
async def read_all_cartoon_characters(db: Session = Depends(get_db)):
    return db.query(models.CartoonCharacter).all()


@router.get("/api/disney/read/{cartoon_character_id}/")
async def read_cartoon_character(cartoon_character_id: int, db: Session = Depends(get_db)):
    cartoon_character_model = db.query(models.CartoonCharacter)\
        .filter(models.CartoonCharacter.id == cartoon_character_id)\
        .first()

    if cartoon_character_model is not None:
        return cartoon_character_model
    raise http_exception()


@router.get("/api/disney/search/{cartoon_character_name}/")
async def search_cartoon_character(cartoon_character_name: str, db: Session = Depends(get_db)):
    cartoon_character_model = db.query(models.CartoonCharacter)\
        .filter(func.lower(models.CartoonCharacter.character_name) == cartoon_character_name.lower())\
        .first()

    if cartoon_character_model is not None:
        return cartoon_character_model
    raise http_exception()


# Create
@router.post("/api/disney/create/")
async def create_cartoon_character(character: Character, db: Session = Depends(get_db)):
    character_model = models.CartoonCharacter()
    character_model.character_name = character.character_name
    character_model.first_appearance = character.first_appearance
    character_model.first_appearance_title = character.first_appearance_title
    character_model.species = character.species
    character_model.gender = character.gender

    db.add(character_model)
    db.commit()

    return success_response(201)


# Update
@router.put("/api/disney/update/{cartoon_character_id}")
async def update_character(cartoon_character_id: int, character: Character, db: Session = Depends(get_db)):
    character_model = db.query(models.CartoonCharacter)\
        .filter(models.CartoonCharacter.id == cartoon_character_id)\
        .first()

    if character_model is None:
        raise http_exception()

    character_model.character_name = character.character_name
    character_model.first_appearance = character.first_appearance
    character_model.first_appearance_title = character.first_appearance_title
    character_model.species = character.species
    character_model.gender = character.gender

    db.add(character_model)
    db.commit()

    return success_response(200)


# Delete
@router.delete("/api/warner/delete/{cartoon_character_id}")
async def delete_cartoon_character(cartoon_character_id: int, db: Session = Depends(get_db)):
    character_model = db.query(models.CartoonCharacter)\
        .filter(models.CartoonCharacter.id == cartoon_character_id)\
        .first()

    if character_model is None:
        raise http_exception()

    db.query(models.CartoonCharacter)\
        .filter(models.CartoonCharacter.id == cartoon_character_id)\
        .delete()

    db.commit()

    return success_response(200)


# Error handling
def http_exception():
    return HTTPException(status_code=404, detail="Record not found.")


def success_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }
