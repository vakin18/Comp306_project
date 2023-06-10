import repository.Repository as Repo
from constants import DB, COURSE_TUPLES, CourseModel

def initializeCourseTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.courses}( 
    code VARCHAR(50),
    name VARCHAR(50),
    headtutor_name VARCHAR(50),
    PRIMARY KEY (code),
    FOREIGN KEY (headtutor_name) REFERENCES {DB.users}(username));'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateCourseTable()
    return


def populateCourseTable():
    c, conn = Repo.getCursorAndConnection()

    for course in COURSE_TUPLES:
        if not courseExistsByCode(course[CourseModel.code]):
            createCourse(*course)
            

    conn.commit()
    conn.close()

def createCourse(code: str, name: str, headtutor_name: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"INSERT INTO {DB.courses} (code, name, headtutor_name) VALUES (?, ?, ?)",
        (code, name, headtutor_name)
    )
    conn.commit()
    conn.close()

def getCourseByCode(code: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"SELECT * FROM {DB.courses} WHERE code = ?", (code,))

    user = c.fetchone()
    conn.commit()
    conn.close()
    return user

def courseExistsByCode(code: str):
    course = getCourseByCode(code)

    return not (course is None)

def updateHeadTutorToCourse(courseCode: str, headTutorName: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"UPDATE {DB.courses} "
        f"SET headtutor_name = {headTutorName}"
        f"WHERE code = {courseCode}")
    conn.commit()
    conn.close()
