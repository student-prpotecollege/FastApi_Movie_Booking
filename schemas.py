from pydantic import BaseModel

class MovieCreate(BaseModel):
    name: str
    genre: str

class ShowCreate(BaseModel):
    movie_id: int
    theatre_id: int
    time: str
    seats: int

class BookingCreate(BaseModel):
    user_id: int
    show_id: int
    seats: int