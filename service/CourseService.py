import repository.CourseRepository as CR

def getAllCourses():
    courses_tuples = CR.getAllCourses()
    courses_list = [course[0] for course in courses_tuples]
    return courses_list

def updateHeadTutorToCourse(courseCode: str, headTutorName: str):
    return CR.updateHeadTutorToCourse(courseCode, headTutorName)