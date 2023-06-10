import repository.Repository as Repo
from constants import DB, CUBICLE_TUPLES, CubicleModel

def initializeCubicleTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.cubicles}( 
    cubicle_number VARCHAR(10),
    location VARCHAR(50),
    PRIMARY KEY (cubicle_number));'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateCubicleTable()
    return


def populateCubicleTable():
    c, conn = Repo.getCursorAndConnection()

    for cubicle in CUBICLE_TUPLES:
        if not cubicleExists(cubicle[CubicleModel.cubicle_number]):
            createCubicle(*cubicle)
            
    conn.commit()
    conn.close()

def createCubicle(cubicle_number: str, location: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"INSERT INTO {DB.cubicles} (cubicle_number, location) VALUES (?, ?)",
        (cubicle_number, location)
    )
    conn.commit()
    conn.close()

def getCubicleByNumber(cubicle_number: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"SELECT * FROM {DB.cubicles} WHERE cubicle_number = ?", (cubicle_number,))

    cubicle = c.fetchone()
    conn.commit()
    conn.close()
    return cubicle

def cubicleExists(cubicle_number: str):
    cubicle = getCubicleByNumber(cubicle_number)

    return not (cubicle is None)


def getAllCubicles():
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"SELECT cubicle_number FROM {DB.cubicles}")
    
    cubicles = c.fetchall()
    conn.close()

    return cubicles