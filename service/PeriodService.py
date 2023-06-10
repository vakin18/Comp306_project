from constants import PeriodModel
import repository.PeriodRepository as PR

def periodToString(periods):
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
    periods = []
    for period_string in period_strings:
        day, interval = period_string.split(', ')
        periods.append((day, interval))

    return periods

def createPeriod(day, interval):
    period_exists = PR.periodExists(day, interval)
    if period_exists:
        # TODO: Handle
        print("This period already exists. Cannot create")
        return
    
    PR.createPeriod(day, interval)
    return

def getDayAndInterval(period_id):
    print(f'period id: {period_id}')
    day, interval = PR.getDayAndInterval(period_id)
    period_string = periodToString([(day, interval)])[0]

    return period_string
