import repository.UserRepository as UR
import repository.CourseRepository as CR
import repository.PeriodRepository as PR
import repository.TutorPeriodRepository as TPR
import repository.CourseTutorRepository as CTR

UR.initializeUserTable()
UR.initializeTutorTable()
CR.initializeCourseTable()
PR.initializePeriodTable()
TPR.initializeTutorPeriodTable()
CTR.initializeCourseTutorTable()