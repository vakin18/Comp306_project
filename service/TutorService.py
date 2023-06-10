from repository import CourseTutorRepository as CTR, UserRepository as UR

def getAllTutors():
    tutors = UR.getAllTutors()
    return tutors

def getTutorByCourse(courseCode: str):
    tutors = CTR.getTutorsByCourse(courseCode)
    return tutors
