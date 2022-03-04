from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from enum import Enum


router = APIRouter()


# Pydantic Models
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-Binary"


class Character(BaseModel):
    id: UUID
    character_name: str = Field(min_length=1)
    first_appearance: date = Field(default='2000-01-01')
    first_appearance_title: Optional[str] = Field(title="First cartoon character appeared in",
                                                  max_length=100,
                                                  min_length=1,
                                                  default=None)
    species: Optional[str] = Field(min_length=1, max_length=100)
    gender: Gender = Gender.MALE
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "91a21fcb-e6e3-4f4e-be79-0b33d3ee2a6f",
                "character_name": "Porky Pig",
                "first_appearance": "1935-03-02",
                "first_appearance_title": "I Haven't Got a Hat",
                "species": "Pig",
                "gender": "Male",
                "rating": 50
            }
        }


WARNER_CHARACTERS = []


# Read
@router.get("/api/warner/read")
async def list_all_characters(characters_to_return: Optional[int] = None):
    if len(WARNER_CHARACTERS) < 1:
        create_characters_no_api()

    if characters_to_return and len(WARNER_CHARACTERS) >= characters_to_return > 0:
        i = 1
        new_characters = []
        while i <= characters_to_return:
            new_characters.append(WARNER_CHARACTERS[i - 1])
            i += 1
        return new_characters

    return WARNER_CHARACTERS


@router.get("/api/warner/read/{character_id}")
async def get_character_by_id(character_id: UUID):
    for character in WARNER_CHARACTERS:
        if character.id == character_id:
            return character
    raise raise_record_cannot_be_found_exception()


@router.get("/api/warner/search/{search_name}")
async def search_character_by_name(search_name: str):
    for character in WARNER_CHARACTERS:
        if character.character_name.lower() == search_name.lower():
            return character
    raise raise_record_cannot_be_found_exception()


# Update
@router.put("/api/warner/update/{character_id}")
async def update_character(character_id: UUID, character: Character):
    counter = 0

    for record in WARNER_CHARACTERS:
        counter += 1
        if record.id == character_id:
            WARNER_CHARACTERS[counter - 1] = character
            return WARNER_CHARACTERS[counter - 1]
    raise raise_record_cannot_be_found_exception()


# Create
@router.post("/api/warner/create/")
async def create_character(character: Character):
    WARNER_CHARACTERS.append(character)
    return character


# Delete
@router.delete("/api/warner/delete/{character_id}")
async def delete_book(character_id: UUID):
    counter = 0

    for record in WARNER_CHARACTERS:
        counter += 1
        if record.id == character_id:
            del WARNER_CHARACTERS[counter - 1]
            return f'character_id: {character_id} deleted'
    raise raise_record_cannot_be_found_exception()


# Add data
def create_characters_no_api():
    charater_1 = Character(id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                           character_name="Wile E. Coyote",
                           first_appearance="1949-09-17",
                           first_appearance_title="Fast and Furry-ous",
                           species="Coyote",
                           gender="Male",
                           rating=90)
    charater_2 = Character(id="e5a9a6c6-5cef-4c75-b7d5-59fafb67e0c3",
                           character_name="Bugs Bunny",
                           first_appearance="1938-04-30",
                           first_appearance_title="A Wild Hare",
                           species="Rabbit",
                           gender="Male",
                           rating=80)
    charater_3 = Character(id="bdd19684-8a3f-48d0-b9a3-27b7a6b7defe",
                           character_name="Daffy Duck",
                           first_appearance="1937-04-17",
                           first_appearance_title="Porky Duck Hunt",
                           species="Duck",
                           gender="Male",
                           rating=70)
    WARNER_CHARACTERS.append(charater_1)
    WARNER_CHARACTERS.append(charater_2)
    WARNER_CHARACTERS.append(charater_3)


# Error Handling
def raise_record_cannot_be_found_exception():
    raise HTTPException(status_code=404,
                        detail="Record not found.",
                        headers={"X-Header-Error": "Does not exist."})
