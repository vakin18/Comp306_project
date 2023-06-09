from constants import PeriodModel
import repository.PeriodRepository as PR

def periodToString(periods):
    periodStrings = []
    for period in periods:
        periodStrings.append(f'{period[PeriodModel.day]}, {period[PeriodModel.interval]}')

    return periodStrings


def getAllPeriods():
    period_tuples = PR.getAllPeriods()
    return period_tuples

def stringToPeriod(period_strings):
    periods = []
    for period_string in period_strings:
        day, interval = period_string.split(', ')
        periods.append((day, interval))

    return periods
