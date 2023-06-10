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

    #TODO:Populate

    conn.commit()
    conn.close()

def getTutorsByCourse(courseCode: str):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT tutor_name FROM {DB.course_tutor} WHERE course_code = {courseCode}")

    result = c.fetchall()
    conn.close()
    return result
