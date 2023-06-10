import repository.Repository as Repo
from constants import DB, COURSE_TUTOR_TUPLES


def initializeCourseTutorTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.course_tutor}( 
        course_code VARCHAR(50),
        tutor_name VARCHAR(50),
        PRIMARY KEY (course_code, tutor_name),
        FOREIGN KEY (course_code) REFERENCES {DB.courses}(code),
        FOREIGN KEY (tutor_name) REFERENCES {DB.tutors}(username))'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateCourseTutorTable()


def populateCourseTutorTable():
    c, conn = Repo.getCursorAndConnection()

    for course_tutor in COURSE_TUTOR_TUPLES:
        if not courseTutorExists(*course_tutor):
            createCourseTutor(*course_tutor)

    conn.commit()
    conn.close()

def getTutorsByCourse(courseCode: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT tutor_name FROM {DB.course_tutor} WHERE course_code = '{courseCode}'")

    result = c.fetchall()
    conn.close()
    return result

def createCourseTutor(course_code, tutor_name):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"INSERT INTO {DB.course_tutor} (course_code, tutor_name) VALUES (?, ?)",
        (course_code, tutor_name)
    )
    conn.commit()
    conn.close()


def courseTutorExists(course_code, tutor_name):
    c, conn = Repo.getCursorAndConnection()

    c.execute(
        f"SELECT * FROM {DB.course_tutor} WHERE course_code = ? and tutor_name = ?", (course_code, tutor_name))

    course_tutor = c.fetchone()
    conn.close()
    return not (course_tutor is None)