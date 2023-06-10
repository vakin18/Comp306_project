import repository.TutorPeriodRepository as TPR
import repository.PeriodRepository as PR
import service.UserService as US
import service.PeriodService as PS
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
    return

def getPeriodsByTutor(selected_tutor):
    period_ids = TPR.getPeriodsByTutor(selected_tutor)
    
    period_strings = []

    for period_id in period_ids:
        period_strings.append(PS.getDayAndInterval(period_id))

    return period_strings
    
def unassignPeriod(selected_tutor, assigned_period_string):
    day, interval = PS.stringToPeriod([assigned_period_string])[0]
    period_id = PS.getPeriod(day, interval)[PeriodModel.id]

    print(f'selected_tutor: {selected_tutor}, period_id: {period_id}')
    TPR.unassignPeriod(selected_tutor, period_id)
    return