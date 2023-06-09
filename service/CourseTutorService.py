import repository.CourseTutorRepository as CTR
import service.CourseService as CS
import service.UserService as US
import service.TutorService as TS
from constants import CourseModel

def createCourseTutor(course_code, tutor_name):
    course_exists = CS.courseExistsByCode(course_code)
    error_message = ""
    if not course_exists:
        
        error_message = "This course does not exist. Cannot assign"
        return error_message
    
    tutor_exists = US.isTutorByUsername(tutor_name)
    if not tutor_exists:
       
        error_message = "This tutor does not exist. Cannot assign"
        return error_message
    
    course_tutor_exists = CTR.courseTutorExists(course_code, tutor_name)
    if course_tutor_exists:
        
        error_message = f"This course is already assigned to {tutor_name}. Cannot assign"
        return error_message
    
    CTR.createCourseTutor(course_code, tutor_name)
    return error_message


def getCoursesByTutor(tutor_name):
    courses_tuple = CTR.getCoursesByTutor(tutor_name)
    courses_list = [course[CourseModel.code] for course in courses_tuple]
    return courses_list


def unassignCourse(tutor_name: str, course_code: str):
    tutor_exists = US.isTutorByUsername(tutor_name)
    error_message = ""
    if not tutor_exists:
        
        error_message = "There is no such tutor. Cannot unassign course"
        return error_message
    
    course_exists = CS.courseExistsByCode(course_code)
    if not course_exists:
        
        error_message = "There is no such course in the system."
        return error_message

    is_course_assigned = CTR.courseTutorExists(course_code, tutor_name)
    if not is_course_assigned:
        
        error_message = "This course is not assigned to this tutor. Cannot unassign."
        return error_message

    CTR.unassignCourse(course_code, tutor_name)
    CS.updateHeadTutorIfNeeded(course_code, tutor_name)
    TS.removeTutorIfNoCourse(tutor_name)

    return error_message

def getTutorsByCourse(courseCode: str):
    return CTR.getTutorsByCourse(courseCode)



    