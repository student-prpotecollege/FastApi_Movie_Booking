from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)

class Theatre(Base):
    __tablename__ = "theatres"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    theatre_id = Column(Integer, ForeignKey("theatres.id"))
    time = Column(String)
    available_seats = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    show_id = Column(Integer)
    seats = Column(Integer)