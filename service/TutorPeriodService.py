import repository.TutorPeriodRepository as TPR
import repository.PeriodRepository as PR
from constants import PeriodModel

def createTutorPeriod(tutor_username, day, interval):
    period = PR.getPeriod(day, interval)
    if not period:
        # TODO: handle when period does not exist
        return

    period_id = period[PeriodModel.id]
    TPR.createTutorPeriod(tutor_username, period_id)