def calculate_grade(avg):
    """Return grade based on average marks."""
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

def print_report_card(student):
    """Display formatted report card for a student."""
    print("\n" + "="*40)
    print(f"        STUDENT REPORT CARD")
    print("="*40)
    """print(f"Student ID : {student['sid']}")"""
    print(f"Name       : {student['name']}")
    print(f"Subjects   :")
    for subject, mark in student['marks'].items():
        print(f"  - {subject}: {mark}")
    print("-"*40)
    print(f"Total Marks: {student['total']}")
    print(f"Average    : {student['average']:.2f}")
    print(f"Grade      : {student['grade']}")
    print("="*40 + "\n")

def main():
    students = {}
    n = int(input("Enter number of students: "))
    for i in range(n):
        print(f"Entering details for student {i+1}:")
        sid=input("Enter student ID: ")
        name = input("Enter student name: ")
        marks={}
        m=int(input("Enter number of subjects: "))
        for j in range(m):
            subject = input(f"Subject {j+1} name: ")
            mark = float(input(f"Marks for {subject}: "))
            marks[subject] = mark
        total = sum(marks.values())
        average = total / m
        grade = calculate_grade(average)
        students[sid] = {
            'name': name,
            'marks': marks,
            'total': total,
            'average': average,
            'grade': grade
        }


    print("\n\n======= ALL STUDENT REPORT CARDS =======")
    for sid, student in students.items():
        print_report_card(student)

if __name__ == "__main__":
    main()