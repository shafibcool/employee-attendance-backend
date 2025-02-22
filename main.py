from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Attendance

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Employee Attendance API is running!"}

@app.post("/mark-attendance/")
def mark_attendance(employee_name: str, date: str, status: str, location: str, db: Session = Depends(get_db)):
    new_entry = Attendance(employee_name=employee_name, date=date, status=status, location=location)
    db.add(new_entry)
    db.commit()
    return {"message": "Attendance marked successfully!"}

@app.get("/attendance/")
def get_attendance(location: str, db: Session = Depends(get_db)):
    records = db.query(Attendance).filter(Attendance.location == location).all()
    return records

# Initialize DB on startup
init_db()
