import repository.TutorPeriodRepository as TPR
import repository.PeriodRepository as PR
import service.UserService as US
import service.PeriodService as PS
from constants import PeriodModel

DEBUG = True

def createTutorPeriod(tutor_username, day, interval):
    period = PR.getPeriod(day, interval)
    error_message = ""
    if not period:
        error_message = "This period does not exist"
        
        return error_message
    period_id = period[PeriodModel.id]

    tutor_exists = US.isTutorByUsername(tutor_username)
    if not tutor_exists:
        error_message = "This tutor does not exist"
        
        return error_message

    tutor_period_exists = TPR.tutorPeriodExists(tutor_username, period_id)
    if tutor_period_exists:
        error_message = "This tutor-period assignment already exists"
        
        return error_message

    TPR.createTutorPeriod(tutor_username, period_id)
    return error_message

def getPeriodsByTutor(selected_tutor):
    period_ids = TPR.getPeriodsByTutor(selected_tutor)
    
    period_strings = []

    for period_id in period_ids:
        period_strings.append(PS.getDayAndInterval(period_id))

    return period_strings
    
def unassignPeriod(selected_tutor, assigned_period_string):
    day, interval = PS.stringToPeriod([assigned_period_string])[0]
    period_id = PS.getPeriod(day, interval)[PeriodModel.id]

    TPR.unassignPeriod(selected_tutor, period_id)
    return

def getTutorPeriod(tutor_username, period_id):
    tp = TPR.getTutorPeriod(tutor_username, period_id)
    return tp