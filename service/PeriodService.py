from constants import PeriodModel
import repository.PeriodRepository as PR

def periodToString(periods):
    # Expects only day and interval
    periodStrings = []
    for period in periods:
        periodStrings.append(f'{period[0]}, {period[1]}')

    return periodStrings


def getAllPeriods():
    period_tuples = PR.getAllPeriods()
    return period_tuples

def getPeriod(day, interval):
    return PR.getPeriod(day, interval)


def stringToPeriod(period_strings):
    # Expects day, interval
    periods = []
    for period_string in period_strings:
        day, interval = period_string.replace(' ', '').split(',')
        periods.append((day, interval))

    return periods

def createPeriod(day, interval):
    period_exists = PR.periodExists(day, interval)
    error_message = ""
    if period_exists:
        
        error_message = "This period already exists. Cannot create"
        return error_message
    
    PR.createPeriod(day, interval)
    return

def getDayAndInterval(period_id):
    print(f'period id: {period_id}')
    day, interval = PR.getDayAndInterval(period_id)
    period_string = periodToString([(day, interval)])[0]

    return period_string


def deletePeriodByDayAndInterval(day: str, interval: str):
    period_exists = PR.periodExists(day, interval)
    error_message = ""
    if not period_exists:
        
        error_message = "This day-interval period does not exist. Cannot remove"
        return error_message
    
    PR.deletePeriodByDayAndInterval(day, interval)