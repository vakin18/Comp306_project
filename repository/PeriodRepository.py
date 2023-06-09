import repository.Repository as Repo
from constants import DB, PERIOD_TUPLES, PeriodModel

def initializePeriodTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.periods}(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day VARCHAR(10) CHECK (day IN ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")),
    interval VARCHAR(12) CHECK (interval IN ("10:00-11:00","11:00-12:00","12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00")));'''

    c.execute(query)
    conn.commit()
    conn.close()

    populatePeriodTable()
    return


def populatePeriodTable():
    c, conn = Repo.getCursorAndConnection()

    for period in PERIOD_TUPLES:
        if not periodExists(period[0], period[1]):
            createPeriod(*period)
            
    conn.commit()
    conn.close()

def createPeriod(day, interval):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"INSERT INTO {DB.periods} (day, interval) VALUES (?, ?)",
        (day, interval)
    )
    conn.commit()
    conn.close()

def getPeriod(day, interval):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"SELECT * FROM {DB.periods} WHERE day = ? and interval = ?", (day, interval))

    period = c.fetchone()
    conn.close()
    return period

def periodExists(day, interval):
    period = getPeriod(day, interval)

    return not (period is None)