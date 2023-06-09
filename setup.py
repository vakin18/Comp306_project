import repository.UserRepository as UR
import repository.CourseRepository as CR
import repository.PeriodRepository as PR

UR.initializeUserTable()
UR.initializeTutorTable()
CR.initializeCourseTable()
PR.initializePeriodTable()
