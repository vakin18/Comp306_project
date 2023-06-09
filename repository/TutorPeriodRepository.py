import repository.Repository as Repo
from constants import DB, PERIOD_TUPLES, PeriodModel

def initializePeriodTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.tutor_period}(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_username VARCHAR(50),
    period_id INTERGER,
    FOREIGN KEY (tutor_username) REFERENCES {DB.tutors}(username),
    FOREIGN KEY (period_id) REFERENCES {DB.periods}(id),
    );'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateTutorPeriodTable()
    return


def populateTutorPeriodTable():
    # c, conn = Repo.getCursorAndConnection()

    # for period in PERIOD_TUPLES:
    #     if not periodExists(period[0], period[1]):
    #         createPeriod(*period)
            
    # conn.commit()
    # conn.close()
    return

def createTutorPeriod(tutor_username, period_id):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"INSERT INTO {DB.tutor_period} (tutor_username, period_id) VALUES (?, ?)",
        (tutor_username, period_id)
    )
    conn.commit()
    conn.close()

def getTutorPeriod(tutor_username, period_id):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"SELECT * FROM {DB.tutor_period} WHERE day = ? and interval = ?", (tutor_username, period_id))

    period = c.fetchone()
    conn.close()
    return period

def tutorPeriodExists(tutor_username, period_id):
    tutor_period = getTutorPeriod(tutor_username, period_id)

    return not (tutor_period is None)
