import repository.Repository as Repo
import repository.PeriodRepository as PR
from constants import DB, PeriodModel

def initializeTutorPeriodCubicleTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.tp_cubicle}(
    id INTEGER PRIMARY KEY,
    cubicle_number VARCHAR(10),
    FOREIGN KEY (cubicle_number) REFERENCES {DB.cubicles}(cubicle_number) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES {DB.tutor_period}(id) ON DELETE CASCADE
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
    c.execute(
        f"SELECT id FROM {DB.tutor_period} WHERE tutor_username = ? AND period_id = ?",
        (tutor_username, period_id)
    )

    id = c.fetchone()

    c.execute(
        f"INSERT INTO {DB.tp_cubicle} (id, cubicle_number) VALUES (?, ?)",
        (id, cubicle_number)
    )
    conn.commit()
    conn.close()

def getTutorPeriodCubicle(id, cubicle_number):
    c, conn = Repo.getCursorAndConnection()
    
    #gets id from tutor_period
    c.execute(
        f"SELECT id FROM {DB.tp_cubicle} WHERE id = ? and cubicle_number = ?", (id, cubicle_number))

    id = c.fetchone()

    c.execute(
        f"SELECT cubicle_number FROM {DB.tp_cubicle} WHERE id = ?",
        (id)
    )

    cubicle_number = c.fetchone()

    conn.close()
    return cubicle_number

def tutorPeriodCubicleExists(id, cubicle_number):
    tp_cubicle = getTutorPeriodCubicle(id, cubicle_number)

    return not (tp_cubicle is None)



def getFreeCubicles(period_id):

    c, conn = Repo.getCursorAndConnection()

    
    c.execute(f"SELECT cubicle_number FROM {DB.cubicles}"
               f" WHERE cubicle_number NOT IN "
               f" (SELECT cubicle_number FROM {DB.tp_cubicle}, {DB.tutor_period}" 
               f" WHERE {DB.tp_cubicle}.id={DB.tutor_period}.id AND {DB.tutor_period}.period_id='{period_id}') ORDER BY cubicle_number ASC")

    result = c.fetchall()
    conn.close()
    return result

def unassignPeriod(selected_tutor, assigned_period):
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"DELETE FROM {DB.tutor_period} WHERE tutor_username = '{selected_tutor}' and period_id = {assigned_period}")

    conn.commit()
    conn.close()
    return