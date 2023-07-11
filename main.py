class Grade:
    def __init__(self, student_id, student_name, course_code, assignment_name, score):
        self.student_id = student_id
        self.student_name = student_name
        self.course_code = course_code
        self.assignment_name = assignment_name
        self.score = score


class GradeTracker:
    def __init__(self):
        self.students = []
        self.courses = []
        self.grades = []

    def add_student(self, name, student_id):
        student = Student(name, student_id)
        self.students.append(student)

    def add_course(self, course_code, course_name):
        course = Course(course_code, course_name)
        self.courses.append(course)

    def add_grade(self, student_id, student_name, course_code, assignment_name, score):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_code(course_code)

        if student is None or course is None:
            return False

        # Validate score input
        if not self.validate_score(score):
            return False

        # Create a new Grade object
        grade = Grade(student_id, student_name, course_code, assignment_name, score)

        # Add the grade to the grades list
        self.grades.append(grade)

        return True

    def calculate_weighted_average_grade(self, student_id, course_code):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_code(course_code)

        if student is None or course is None:
            return None

        # Filter grades for the specific student and course
        filtered_grades = [grade for grade in self.grades if
                           grade.student_id == student_id and grade.course_code == course_code]

        if len(filtered_grades) == 0:
            return None

        # Prompt the user for the number of assignments and their respective weights
        num_assignments = self.get_valid_integer_input("Enter the number of assignments: ")
        if num_assignments <= 0:
            print("Number of assignments must be a positive integer.")
            return None

        assignment_weights = {}
        total_weight = 0
        for i in range(num_assignments):
            assignment_name = input(f"Enter assignment name {i+1}: ")
            weight = self.get_valid_integer_input(f"Enter the weight of assignment {i+1} out of 100: ")
            if weight < 0 or weight > 100:
                print("Weight must be between 0 and 100.")
                return None

            assignment_weights[assignment_name] = weight
            total_weight += weight

        weighted_sum = 0
        for grade in filtered_grades:
            assignment_weight = assignment_weights.get(grade.assignment_name)
            weighted_sum += (grade.score * assignment_weight)

        average = weighted_sum / total_weight
        return average

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

    @staticmethod
    def get_valid_integer_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please enter an integer.")


class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id


class Course:
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name


# Example usage

# Create a GradeTracker instance
grade_tracker = GradeTracker()

# Add students
name = input("Enter student name: ")
student_id = input("Enter student ID: ")
grade_tracker.add_student(name, student_id)

# Add courses
course_code = input("Enter course code: ")
course_name = input("Enter course name: ")
grade_tracker.add_course(course_code, course_name)

# Add grades
num_assignments = grade_tracker.get_valid_integer_input("Enter the number of assignments: ")
if num_assignments <= 0:
    print("Number of assignments must be a positive integer.")
else:
    for i in range(num_assignments):
        assignment_name = input(f"Enter assignment name {i+1}: ")
        score = input(f"Enter score for assignment {i+1}: ")

        if not grade_tracker.validate_score(score):
            print("Invalid score. Please try again.")
            break

        grade_tracker.add_grade(student_id, name, course_code, assignment_name, float(score))

    else:
        # Calculate weighted average grade
        average_grade = grade_tracker.calculate_weighted_average_grade(student_id, course_code)
        if average_grade is not None:
            print(f"Course mark for {name} in {course_name}: {average_grade}")
        else:
            print("No marks found for the student and course combination.")
