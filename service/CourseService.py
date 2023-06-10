import repository.CourseRepository as CR

def createCourse(code, name, headtutor_name):
    CR.createCourse(code, name, headtutor_name)

def getAllCourses():
    courses_tuples = CR.getAllCourses()
    courses_list = [course[0] for course in courses_tuples]
    return courses_list

def courseExistsByCode(code: str):
    return CR.courseExistsByCode(code)


def updateHeadTutorToCourse(courseCode: str, headTutorName: str):
    return CR.updateHeadTutorToCourse(courseCode, headTutorName)
