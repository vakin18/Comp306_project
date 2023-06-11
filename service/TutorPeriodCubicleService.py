import repository.TutorPeriodCubicleRepository as TPCR
import repository.PeriodRepository as PR
import service.UserService as US
import service.PeriodService as PS
from constants import PeriodModel

DEBUG = True

def createTutorPeriodCubicle(tutor, day, interval, cubicle):
    period = PR.getPeriod(day, interval)
    if not period:
        # TODO: handle when period does not exist
        if DEBUG:
            print("This period does not exist")
        return
    period_id = period[PeriodModel.id]

    tutor_exists = US.isTutorByUsername(tutor)
    if not tutor_exists:
        # TODO: handle when tutor does not exist
        if DEBUG:
            print("This tutor does not exist")
        return

    print(f'period_id : {period_id}')
    tutor_period_cubicle_exists = TPCR.tutorPeriodCubicleExists(period_id, cubicle)
    if tutor_period_cubicle_exists:
        # TODO: handle when tutor-period already exists
        if DEBUG:
            print("This tutor-period-cubicle assignment already exists")
        return

    TPCR.createTutorPeriodCubicle(tutor, period_id)
    return

    
def getFreeCubicles(day, interval):

    period = PR.getPeriod(day, interval)
    if not period:
        # TODO: handle when period does not exist
        if DEBUG:
            print("This period does not exist")
        return
    period_id = period[PeriodModel.id]

    cubicles_tuples = TPCR.getFreeCubicles(period_id)

    cubicle_list = [cubicle[0] for cubicle in cubicles_tuples]

    

    return cubicle_list