from repository import CourseTutorRepository as CTR, UserRepository as UR

def getAllTutors():
    tutors_tuple = UR.getAllTutors()
    tutors_list = [tutor[0] for tutor in tutors_tuple]
    return tutors_list

def getTutorByCourse(courseCode: str):
    tutors_tuple = CTR.getTutorsByCourse(courseCode)
    tutors_list = [tutor[0] for tutor in tutors_tuple]
    return tutors_list

def removeTutorIfNoCourse(tutor_name: str):
    UR.removeTutorIfNoCourse(tutor_name)

def removeTutorsWithNoCourse():
    UR.removeTutorsWithNoCourse()
    