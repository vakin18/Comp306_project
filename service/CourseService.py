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

def deleteCourse(code):
    course_exists = courseExistsByCode(code)

    error_message = ""
    if not course_exists:
        
        error_message = "This course does not exist. Cannot remove"
        return error_message
    
    CR.deleteCourse(code)

    return error_message

def updateHeadTutorIfNeeded(course_code, tutor_name):
    """
    Update head tutor to null if course.head_tutor = tutor_name
    """
    CR.updateHeadTutorIfNeeded(course_code, tutor_name)
    return