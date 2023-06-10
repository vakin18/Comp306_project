import repository.UserRepository as UR
import repository.CourseRepository as CR
import repository.PeriodRepository as PR
import repository.TutorPeriodRepository as TPR
import repository.CourseTutorRepository as CTR
import repository.CubicleRepository as CubR

UR.initializeUserTable()
UR.initializeTutorTable()
CR.initializeCourseTable()
PR.initializePeriodTable()
TPR.initializeTutorPeriodTable()
CTR.initializeCourseTutorTable()
CubR.initializeCubicleTable()