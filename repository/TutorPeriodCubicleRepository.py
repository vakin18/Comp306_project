import repository.Repository as Repo
import repository.PeriodRepository as PR
import service.TutorPeriodService as TPS
from constants import DB, PeriodModel

def initializeTutorPeriodCubicleTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.tp_cubicle}(
    tp_id INTEGER,
    cubicle_number VARCHAR(10),
    PRIMARY KEY (tp_id, cubicle_number)
    FOREIGN KEY (cubicle_number) REFERENCES {DB.cubicles}(cubicle_number) ON DELETE CASCADE,
    FOREIGN KEY (tp_id) REFERENCES {DB.tutor_period}(id) ON DELETE CASCADE
    );'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateTutorPeriodCubicleTable()
    return


def populateTutorPeriodCubicleTable():
    # c, conn = Repo.getCursorAndConnection()

    # for period in PERIOD_TUPLES:
    #     if not periodExists(period[0], period[1]):
    #         createPeriod(*period)
            
    # conn.commit()
    # conn.close()
    return

def createTutorPeriodCubicle(tutor_username, period_id, cubicle_number):
    c, conn = Repo.getCursorAndConnection()

    # gets id from tutor_period
    tp = TPS.getTutorPeriod(tutor_username, period_id)
    tp_id = tp[0]

    query = f"INSERT INTO {DB.tp_cubicle} (tp_id, cubicle_number) VALUES ({tp_id}, {cubicle_number})"
    c.execute(query)
    conn.commit()
    conn.close()

def getTutorPeriodCubicle(tutor: str, period_id: int, cubicle_number):
    tp = TPS.getTutorPeriod(tutor, period_id)
    tp_id = tp[0]

    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT * FROM {DB.tp_cubicle} WHERE tp_id = {tp_id} and cubicle_number = '{cubicle_number}'")

    tpc = c.fetchone()

    conn.close()
    return tpc

def tutorPeriodCubicleExists(tutor: str, period_id: int, cubicle_number):
    tp_cubicle = getTutorPeriodCubicle(tutor, period_id, cubicle_number)

    return not (tp_cubicle is None)



def getFreeCubicles(period_id):

    c, conn = Repo.getCursorAndConnection()

    
    c.execute(f"SELECT cubicle_number FROM {DB.cubicles}"
               f" WHERE cubicle_number NOT IN "
               f" (SELECT cubicle_number FROM {DB.tp_cubicle}, {DB.tutor_period}" 
               f" WHERE {DB.tp_cubicle}.tp_id={DB.tutor_period}.id AND {DB.tutor_period}.period_id='{period_id}') ORDER BY cubicle_number ASC")

    result = c.fetchall()
    conn.close()
    return result

def getCubicleByTutorPeriod(tutor_username: str, period_id: str):

    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT cubicle_number FROM {DB.tp_cubicle}"
              f" WHERE tp_id IN"
              f" (SELECT id FROM {DB.tutor_period}"
              f" WHERE tutor_username='{tutor_username}' AND period_id='{period_id}')")
    
    result = c.fetchall()
    conn.close()
    return result