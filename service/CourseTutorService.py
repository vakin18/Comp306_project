import repository.CourseTutorRepository as CTR
import service.CourseService as CS
import service.UserService as US

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