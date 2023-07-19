class Grade:
    def __init__(self, student_id, student_name, course_code, assignment_name, score, weight):
        self.student_id = student_id
        self.student_name = student_name
        self.course_code = course_code
        self.assignment_name = assignment_name
        self.score = score
        self.weight = weight


class GradeTracker:
    def __init__(self):
        self.students = []
        self.courses = []
        self.grades = []

    def add_student(self, name, student_id):
        student = Student(name, student_id)
        self.students.append(student)

    def add_course(self, course_code, course_name, num_assignments, assignment_names):
        course = Course(course_code, course_name, num_assignments, assignment_names)
        self.courses.append(course)
        return course

    def add_grade(self, student_id, student_name, course_code, assignment_name, score, weight):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_code(course_code)

        if student is None or course is None:
            return False

        # Validate score input
        if not self.validate_score(score):
            return False

        # Check if the assignment_name already exists for the student in this course
        existing_assignment_names = [grade.assignment_name for grade in self.grades
                                     if grade.student_id == student_id and grade.course_code == course_code]
        if assignment_name in existing_assignment_names:
            print(f"{assignment_name} already exists for this student in the course.")
            return False

        # Create a new Grade object
        grade = Grade(student_id, student_name, course_code, assignment_name, float(score), weight)

        # Add the grade to the grades list
        self.grades.append(grade)

        return True

    def edit_course_details(self, course_code):
        course = self.find_course_by_code(course_code)

        if course is None:
            return False

        num_assignments = self.get_valid_integer_input("Enter the number of assignments: ")
        if num_assignments <= 0:
            print("Number of assignments must be a positive integer.")
            return False

        course.num_assignments = num_assignments

        for i in range(num_assignments):
            assignment_name = input(f"Enter assignment name {i + 1}: ")
            course.assignment_names.append(assignment_name)

        return True

    def calculate_student_average_grade(self, student_id, course_code):
        student_grades = [grade.score for grade in self.grades if
                          grade.student_id == student_id and grade.course_code == course_code]
        if len(student_grades) == 0:
            return None

        average = sum(student_grades) / len(student_grades)
        return average

    def calculate_course_average_grade(self, course_code):
        course_grades = [grade.score for grade in self.grades if grade.course_code == course_code]
        if len(course_grades) == 0:
            return None

        average = sum(course_grades) / len(course_grades)
        return average

    @staticmethod
    def validate_score(score):
        try:
            score = float(score)
            if 0 <= score <= 100:
                return True
            else:
                print("Score must be between 0 and 100.")
        except ValueError:
            print("Invalid score. Please enter a numeric value.")
        return False

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_course_by_code(self, course_code):
        for course in self.courses:
            if course.course_code == course_code:
                return course
        return None

    @staticmethod
    def get_valid_integer_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please enter an integer.")


def display_student_grades(grade_tracker, student_id, course_code):
    student_grades = [grade for grade in grade_tracker.grades if
                      grade.student_id == student_id and grade.course_code == course_code]

    if len(student_grades) == 0:
        print(f"No grades found for Student ID: {student_id} in Course Code: {course_code}.")
        return

    print(f"\nGrades for Student ID: {student_id} in Course Code: {course_code}:")
    for grade in student_grades:
        print(f"{grade.assignment_name}: {grade.score}")


class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id


class Course:
    def __init__(self, course_code, course_name, num_assignments, assignment_names):
        self.course_code = course_code
        self.course_name = course_name
        self.num_assignments = num_assignments
        self.assignment_names = assignment_names


# Example usage

# Create a GradeTracker instance
grade_tracker = GradeTracker()

# Add course details
course_code = input("Enter course code: ")
course_name = input("Enter course name: ")

num_assignments = int(input("Enter the number of assignments: "))
assignment_names = []
for i in range(num_assignments):
    assignment_name = input(f"Enter assignment name {i + 1}: ")
    assignment_names.append(assignment_name)

# Create a Course object and add it to the GradeTracker
course = grade_tracker.add_course(course_code, course_name, num_assignments, assignment_names)

# Add students and grades
while True:
    name = input("Enter student name: ")
    student_id = input("Enter student ID: ")

    grade_tracker.add_student(name, student_id)

    for assignment_name in course.assignment_names:
        score = input(f"Enter score for {assignment_name}: ")

        while not grade_tracker.validate_score(score):
            score = input("Invalid score. Please enter a valid score: ")

        grade_tracker.add_grade(student_id, name, course_code, assignment_name, float(score), course.num_assignments)

    add_another_student = input("Do you want to add another student? (yes/no): ").lower()
    if add_another_student == 'no':
        break

# Display added students with their respective grades
for student in grade_tracker.students:
    display_student_grades(grade_tracker, student.student_id, course_code)

# Calculate and display average grade for each student
for student in grade_tracker.students:
    average_grade_student = grade_tracker.calculate_student_average_grade(student.student_id, course_code)
    if average_grade_student is not None:
        print(f"\nAverage Grade for Student {student.name} (ID: {student.student_id}): {average_grade_student:.2f}")
    else:
        print(f"\nNo grades found for Student {student.name} (ID: {student.student_id}).")

import pandas as pd

# Calculate and display average grade for the course
average_grade_course = grade_tracker.calculate_course_average_grade(course_code)
if average_grade_course is not None:
    print(f"\nAverage Grade for Course {course_code} ({course_name}): {average_grade_course:.2f}")
else:
    print(f"\nNo grades found for Course {course_code} ({course_name}).")

# Create a DataFrame to store the grades data
data = {
    'Student Name': [],
    'Student ID': [],
    'Grade Average': []
}
for assignment_name in course.assignment_names:
    data[assignment_name] = []

# Add student grades to the DataFrame
for student in grade_tracker.students:
    student_grades = [grade for grade in grade_tracker.grades if
                      grade.student_id == student.student_id and grade.course_code == course_code]

    if len(student_grades) == 0:
        continue

    total_score = 0
    for grade in student_grades:
        data[grade.assignment_name].append(grade.score)
        total_score += grade.score

    average_grade_student = total_score / len(student_grades)
    data['Student Name'].append(student.name)
    data['Student ID'].append(student.student_id)
    data['Grade Average'].append(average_grade_student)

# Create the DataFrame and display it
df = pd.DataFrame(data)
print(df)
