from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
from utils import check_seats

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- USERS ----------------
@app.post("/users/register")
def register_user(name: str, db: Session = Depends(get_db)):
    user = models.User(name=name)
    db.add(user)
    db.commit()
    return user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# ---------------- MOVIES ----------------
@app.post("/movies/add")
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    m = models.Movie(name=movie.name, genre=movie.genre)
    db.add(m)
    db.commit()
    return m

@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()

@app.get("/movies/{id}")
def get_movie(id: int, db: Session = Depends(get_db)):
    return db.query(models.Movie).filter(models.Movie.id == id).first()

@app.put("/movies/{id}")
def update_movie(id: int, data: schemas.MovieCreate, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    movie.name = data.name
    movie.genre = data.genre
    db.commit()
    return {"message": "updated"}

@app.delete("/movies/{id}")
def delete_movie(id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    db.delete(movie)
    db.commit()
    return {"message": "deleted"}

# ---------------- THEATRE ----------------
@app.post("/theatres/add")
def add_theatre(name: str, city: str, db: Session = Depends(get_db)):
    t = models.Theatre(name=name, city=city)
    db.add(t)
    db.commit()
    return t

@app.get("/theatres")
def get_theatres(db: Session = Depends(get_db)):
    return db.query(models.Theatre).all()

# ---------------- SHOW ----------------
@app.post("/shows/create")
def create_show(show: schemas.ShowCreate, db: Session = Depends(get_db)):
    s = models.Show(
        movie_id=show.movie_id,
        theatre_id=show.theatre_id,
        time=show.time,
        available_seats=show.seats
    )
    db.add(s)
    db.commit()
    return s

@app.get("/shows")
def get_shows(db: Session = Depends(get_db)):
    return db.query(models.Show).all()

@app.get("/shows/{id}")
def get_show(id: int, db: Session = Depends(get_db)):
    return db.query(models.Show).filter(models.Show.id == id).first()

@app.get("/shows/by-movie/{movie_id}")
def shows_by_movie(movie_id: int, db: Session = Depends(get_db)):
    return db.query(models.Show).filter(models.Show.movie_id == movie_id).all()

# ---------------- BOOKING ----------------
@app.post("/book-ticket")
def book_ticket(data: schemas.BookingCreate, db: Session = Depends(get_db)):
    show = db.query(models.Show).filter(models.Show.id == data.show_id).first()

    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    if not check_seats(show, data.seats):
        raise HTTPException(status_code=400, detail="Seats not available")

    show.available_seats -= data.seats

    booking = models.Booking(
        user_id=data.user_id,
        show_id=data.show_id,
        seats=data.seats
    )

    db.add(booking)
    db.commit()

    return {"message": "Ticket booked"}

@app.post("/cancel-ticket")
def cancel_ticket(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()

    show = db.query(models.Show).filter(models.Show.id == booking.show_id).first()
    show.available_seats += booking.seats

    db.delete(booking)
    db.commit()

    return {"message": "Cancelled"}

@app.get("/booking/{user_id}")
def booking_history(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

@app.get("/available-seats/{show_id}")
def available_seats(show_id: int, db: Session = Depends(get_db)):
    show = db.query(models.Show).filter(models.Show.id == show_id).first()
    return {"available_seats": show.available_seats}

# ---------------- ADVANCED ----------------
@app.get("/movies/search")
def search_movies(name: str, db: Session = Depends(get_db)):
    return db.query(models.Movie).filter(models.Movie.name.contains(name)).all()

@app.get("/movies/sort")
def sort_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).order_by(models.Movie.name).all()

@app.get("/movies/pagination")
def paginate(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return db.query(models.Movie).offset(skip).limit(limit).all()