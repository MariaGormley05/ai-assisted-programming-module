"""
Buggy Code - Find and fix the bugs!

Instructions:
1. First, try to find the bugs yourself
2. Then ask Copilot: "Review this code for bugs and potential issues"
3. Compare Copilot's findings with yours
4. Ask follow-up questions about specific issues
5. Document your findings

This code is supposed to:
- Read a CSV file of student grades
- Calculate statistics (average, highest, lowest)
- Identify students who need to retake exams (grade < 50)
- Generate a summary report
"""

import csv
from typing import List, Dict


def load_grades(filename: str) -> List[Dict[str, any]]:
    """Load student grades from a CSV file."""
    students = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = {
                'name': row['name'],
                'grade': int(row['grade']),  # Bug: What if the value isn't a valid integer?
                'subject': row['subject']
            }
            students.append(student)
    
    return students


def calculate_average(grades: List[int]) -> float:
    """Calculate the average of a list of grades."""
    total = sum(grades)
    average = total / len(grades)  # Bug: What if grades is empty?
    return average


def find_highest_grade(students: List[Dict[str, any]]) -> Dict[str, any]:
    """Find the student with the highest grade."""
    highest = students[0]  # Bug: What if students is empty?
    
    for student in students:
        if student['grade'] > highest['grade']:
            highest = student
    
    return highest


def find_lowest_grade(students: List[Dict[str, any]]) -> Dict[str, any]:
    """Find the student with the lowest grade."""
    lowest = None
    
    for student in students:
        if lowest is None or student['grade'] < lowest['grade']:
            lowest = student
    
    return lowest


def identify_retakes(students: List[Dict[str, any]]) -> List[str]:
    """Identify students who need to retake (grade < 50)."""
    retakes = []
    
    for student in students:
        if student['grade'] < 50:
            retakes.append(student['name'])
    
    return retakes


def generate_report(students: List[Dict[str, any]]) -> str:
    """Generate a summary report of student grades."""
    if not students:
        return "No student data available"
    
    grades = [s['grade'] for s in students]
    avg = calculate_average(grades)
    highest = find_highest_grade(students)
    lowest = find_lowest_grade(students)
    retakes = identify_retakes(students)
    
    report = f"""
    Grade Report
    ============
    Total Students: {len(students)}
    Average Grade: {avg:.2f}
    Highest Grade: {highest['name']} - {highest['grade']}
    Lowest Grade: {lowest['name']} - {lowest['grade']}  # Bug: What if lowest is None?
    
    Students Needing Retakes ({len(retakes)}):
    """
    
    for name in retakes:
        report += f"\n  - {name}"
    
    return report


def main():
    """Main function to run the grading system."""
    try:
        students = load_grades('grades.csv')  # Bug: File might not exist
        report = generate_report(students)
        print(report)
        
        # Save report to file
        with open('report.txt', 'w') as f:
            f.write(report)
        
        print("\nReport saved to report.txt")
        
    except Exception as e:
        print(f"An error occurred: {e}")  # Bug: Too generic error handling


if __name__ == "__main__":
    main()


# Additional bugs to find:
# 1. No type hints on some functions (any instead of Any)
# 2. No validation for negative grades
# 3. No handling for duplicate students
# 4. Report formatting could be improved
# 5. No logging for debugging
# 6. Magic number 50 for retake threshold should be a constant
# 7. File handling doesn't close files properly in all cases (though 'with' helps)
# 8. No unit tests to catch these bugs!
