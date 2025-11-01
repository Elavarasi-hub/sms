from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Report Card API"}
class Student(BaseModel):
    sid: str
    name: str
    marks: dict 
@app.post("/report-card/")
def generate_report_card(student: Student):
    total_marks = sum(student.marks.values())
    average_marks = total_marks / len(student.marks)
    
    if average_marks >= 90:
        grade = 'A'
    elif average_marks >= 80:
        grade = 'B'
    elif average_marks >= 70:
        grade = 'C'
    elif average_marks >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    report_card = {
        "sid": student.sid,
        "name": student.name,
        "marks": student.marks,
        "total": total_marks,
        "average": average_marks,
        "grade": grade
    }
    
    return report_card

# To run the FastAPI app, use the command:
# uvicorn fastapi:app --reload      
# Save this code in a file named fastapi.py




