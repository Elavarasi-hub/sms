from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session    

# =========================
# DATABASE SETUP
# =========================
DATABASE_URL = "postgresql://postgres:elapapa1@localhost:5432/studentdb"
# For MySQL, use:
# DATABASE_URL = "mysql+mysqlclient://root:yourpassword@localhost:3306/studentdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =========================
# MODEL DEFINITIONS
# =========================
class StudentDB(Base):
    __tablename__ = "students"
    sid = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    marks = Column(JSON, nullable=False)  # store dict as JSON

Base.metadata.create_all(bind=engine)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="Student Management System")


@app.get("/")
async def root():           
    return {"message": "Welcome to the Student Mangemnent System"   }


class StudentMarks(BaseModel):
    marks: Dict[str, float]


class Student(BaseModel):
    sid: int
    name: str
    marks: Dict[str, float]


class StudentsList(BaseModel):
    students: List[Student]

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# db_dependency = Annotetion[Session, "Depends(get_db)"]
# In-memory students store for demo purposes
# NOTE: Hardcoded demo data commented out. Provide students via the API
# (e.g. POST /students/replace or POST /students/append). Keeping
# the store empty by default prevents accidental use of demo data.
# Example (for reference only):
# EXAMPLE_STUDENTS = [
#     {"sid": 1234, "name": "John Doe", "marks": {"Math": 95, "Science": 88, "English": 76}},
#     {"sid": 1235, "name": "Jane Smith", "marks": {"Math": 78, "Science": 85, "English": 80}},
#     {"sid": 1236, "name": "Alice Johnson", "marks": {"Math": 65, "Science": 72, "English": 70}},
# ]

students: List[dict] = []


@app.post("/add-new-student/")
def add_new_students(new_students: List[Student], db: Session = Depends(get_db)):
    for s in new_students:
        db_student = StudentDB(sid=s.sid, name=s.name, marks=s.marks)        
        db.add(db_student)
    db.commit()
    return {"added": len(new_students)}


@app.post("/students/replace")
def replace_students(payload: StudentsList):
    """Replace the entire in-memory students list with the provided list."""
    global students
    students = [s.dict() for s in payload.students]
    return {"message": "students replaced", "count": len(students)}


@app.post("/students/append")
def append_students(payload: StudentsList):
    """Append the provided students to the in-memory list."""
    added = 0
    for s in payload.students:
        students.append(s.dict())
        added += 1
    return {"message": "students appended", "added": added}


@app.get("/get-student/{sid}")
def get_student(sid: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.sid == sid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
    # for student in students:
    #     if student.get('sid') == sid:
    #         return student
    # return {"error": "Student not found"}


@app.put("/update-student/{sid}")
def update_student(sid: int, updated_student: Student, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.sid == sid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = updated_student.name
    student.marks = updated_student.marks
    db.commit()
    db.refresh(student)
    return student


@app.delete("/delete-student/{sid}")
def delete_student(sid: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.sid == sid).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
    
@app.get("/students")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()
    return students

@app.post("/report-card/")
def generate_report_card(student: Student):
    total = sum(student.marks.values())
    average = total / len(student.marks) if student.marks else 0
    grade = calculate_grade(average)

    report_card = {
        "sid": student.sid,
        "name": student.name,
        "marks": student.marks,
        "total": total,
        "average": round(average, 2),
        "grade": grade,
    }
    return report_card


def calculate_grade(avg: float) -> str:
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"      
