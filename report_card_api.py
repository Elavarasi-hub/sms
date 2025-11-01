from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Student Report Card API")

# Pydantic models to validate input
class StudentMarks(BaseModel):
    marks: Dict[str, float]

class Student(BaseModel):
    sid: str
    name: str
    marks: Dict[str, float]

# Grade calculation
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

# API endpoint to calculate report card
@app.post("/report-card/")
def generate_report_card(student: Student):
    total = sum(student.marks.values())
    average = total / len(student.marks)
    grade = calculate_grade(average)
    
    report_card = {
        "sid": student.sid,
        "name": student.name,
        "marks": student.marks,
        "total": total,
        "average": round(average, 2),
        "grade": grade
    }
    return report_card

