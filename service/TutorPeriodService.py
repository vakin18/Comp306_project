import repository.TutorPeriodRepository as TPR
import repository.PeriodRepository as PR
import service.UserService as US
from constants import PeriodModel

DEBUG = True

def createTutorPeriod(tutor_username, day, interval):
    period = PR.getPeriod(day, interval)
    if not period:
        # TODO: handle when period does not exist
        if DEBUG:
            print("This period does not exist")
        return
    period_id = period[PeriodModel.id]

    tutor_exists = US.isTutorByUsername(tutor_username)
    if not tutor_exists:
        # TODO: handle when tutor does not exist
        if DEBUG:
            print("This tutor does not exist")
        return

    tutor_period_exists = TPR.tutorPeriodExists(tutor_username, period_id)
    if tutor_period_exists:
        # TODO: handle when tutor-period already exists
        if DEBUG:
            print("This tutor-period assignment already exists")
        return

    TPR.createTutorPeriod(tutor_username, period_id)