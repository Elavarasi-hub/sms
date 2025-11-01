from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

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
def add_new_students(new_students: List[Student]):
    for s in new_students:
        students.append(s.dict())
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
def get_student(sid: int):
    for student in students:
        if student.get('sid') == sid:
            return student
    return {"error": "Student not found"}


@app.put("/update-student/{sid}")
def update_student(sid: int, updated_student: Student):
    for idx, student in enumerate(students):
        if student.get('sid') == sid:
            students[idx] = updated_student.dict()
            return students[idx]
    return {"error": "Student not found"}


@app.delete("/delete-student/{sid}")
def delete_student(sid: int):
    for student in list(students):
        if student.get('sid') == sid:
            students.remove(student)
            return {"message": "Student deleted successfully"}
    return {"error": "Student not found"}


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
