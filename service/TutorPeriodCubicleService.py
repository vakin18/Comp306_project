import repository.TutorPeriodCubicleRepository as TPCR
import repository.PeriodRepository as PR
import service.UserService as US
import service.PeriodService as PS
from constants import PeriodModel

DEBUG = True

def createTutorPeriodCubicle(tutor, day, interval, cubicle):
    period = PR.getPeriod(day, interval)

    error_message = ""
    if not period:
        

        error_message = "This period does not exist"
        
        return error_message
    period_id = period[PeriodModel.id]

    tutor_exists = US.isTutorByUsername(tutor)
    if not tutor_exists:
        

        error_message = "This tutor does not exist"
        
        return error_message

    tutor_period_cubicle_exists = TPCR.tutorPeriodCubicleExists(tutor, period_id, cubicle)
    if tutor_period_cubicle_exists:
        

        error_message = "This tutor-period-cubicle assignment already exists"
        
        return error_message

    TPCR.createTutorPeriodCubicle(tutor, period_id, cubicle)
    return error_message

    
def getFreeCubicles(day, interval):

    period = PR.getPeriod(day, interval)
    error_message = ""

    if not period:
        
        error_message = "This period does not exist"
        
        return error_message
    period_id = period[PeriodModel.id]

    cubicles_tuples = TPCR.getFreeCubicles(period_id)

    cubicle_list = [cubicle[0] for cubicle in cubicles_tuples]

    

    return error_message, cubicle_list

def getCubicleByTutorPeriod(tutor, day, interval):
    period = PR.getPeriod(day, interval)

    if not period:
        
        #TODO: handle
        print("This period does not exist")
        
        return 
    
    period_id = period[PeriodModel.id]

    cubicles_tuples = TPCR.getCubicleByTutorPeriod(tutor, period_id)

    

    cubicle_list = [cubicle[0] for cubicle in cubicles_tuples]

    return cubicle_list
