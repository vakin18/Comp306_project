import repository.CourseTutorRepository as CTR
import service.CourseService as CS
import service.UserService as US
import service.TutorService as TS
from constants import CourseModel

def createCourseTutor(course_code, tutor_name):
    course_exists = CS.courseExistsByCode(course_code)
    if not course_exists:
        # TODO: handle
        print("This course does not exist. Cannot assign")
        return
    
    tutor_exists = US.isTutorByUsername(tutor_name)
    if not tutor_exists:
        # TODO: handle
        print("This tutor does not exist. Cannot assign")
        return
    
    course_tutor_exists = CTR.courseTutorExists(course_code, tutor_name)
    if course_tutor_exists:
        # TODO: handle
        print(f"This course is already assigned to {tutor_name}. Cannot assign")
        return
    
    CTR.createCourseTutor(course_code, tutor_name)


def getCoursesByTutor(tutor_name):
    courses_tuple = CTR.getCoursesByTutor(tutor_name)
    courses_list = [course[CourseModel.code] for course in courses_tuple]
    return courses_list


def unassignCourse(tutor_name: str, course_code: str):
    tutor_exists = US.isTutorByUsername(tutor_name)
    if not tutor_exists:
        # TODO: handle
        print("There is no such tutor. Cannot unassign course")
        return
    
    course_exists = CS.courseExistsByCode(course_code)
    if not course_exists:
        # TODO: handle
        print("There is no such course in the system.")

    is_course_assigned = CTR.courseTutorExists(course_code, tutor_name)
    if not is_course_assigned:
        # TODO: handle
        print("This course is not assigned to this tutor. Cannot unassign.")

    CTR.unassignCourse(course_code, tutor_name)
    TS.removeTutorIfNoCourse(tutor_name)



    