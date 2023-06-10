from datetime import date
import bcrypt

import repository.Repository as Repo
from constants import DB, USER_TUPLES, STUDENT_TUPLES, TUTOR_TUPLES, UserModel

def initializeUserTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.users}( 
    username VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(50),
    PRIMARY KEY (username));'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateUserTable()
    return

def initializeTutorTable():
    c, conn = Repo.getCursorAndConnection()

    query = f'''CREATE TABLE IF NOT EXISTS {DB.tutors}( 
    username VARCHAR(50),
    start_date DATE NOT NULL, 
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES {DB.users}(username));'''

    c.execute(query)
    conn.commit()
    conn.close()

    populateTutorTable()
    return

def getAllStudents():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT username FROM {DB.users} WHERE role = 'student'")

    result = c.fetchall()
    conn.close()
    return result


def getAllTutors():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT username FROM {DB.tutors}")

    result = c.fetchall()
    conn.close()
    return result

def populateUserTable():
    c, conn = Repo.getCursorAndConnection()

    for user in USER_TUPLES:
        if not userExistsByUsername(user[UserModel.username]):
            createUser(*user)

    for user in STUDENT_TUPLES:
        if not userExistsByUsername(user[UserModel.username]):
            createUser(*user)

    conn.commit()
    conn.close()

def populateTutorTable():
    c, conn = Repo.getCursorAndConnection()

    for tutor in TUTOR_TUPLES:
        if not isTutorByUsername(tutor):
            createTutor(tutor)

    conn.commit()
    conn.close()

def createUser(username: str, email: str, password: str, role: str):
    c, conn = Repo.getCursorAndConnection()
    c.execute(
        f"INSERT INTO {DB.users} (username, email, password, role) VALUES (?, ?, ?, ?)",
        (username, email, encrypt_password(password), role)
    )
    conn.commit()
    conn.close()

def createTutor(username: str):
    c, conn = Repo.getCursorAndConnection()

    today = date.today()
    c.execute(
        f"INSERT INTO {DB.tutors} (username, start_date) VALUES (?, ?)",
        (username, today)
    )
    conn.commit()
    conn.close()

def getUserByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    # Check if the username exists in the database
    c.execute(
        f"SELECT * FROM {DB.users} WHERE username = ?", (username,))

    user = c.fetchone()
    conn.close()
    return user

def getTutorByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    # Check if the username exists in the database
    c.execute(
        f"SELECT * FROM {DB.tutors} WHERE username = ?", (username,))

    user = c.fetchone()
    conn.close()
    return user

def isTutorByUsername(username: str):
    tutor = getTutorByUsername(username)

    return not (tutor is None)

def userExistsByUsername(username: str):
    """
    Return true if a user exists in corresponding database with this username, false otherwise.
    """
    user = getUserByUsername(username)

    return not (user is None)

def removeTutorIfNoCourse(tutor_name: str):
    c, conn = Repo.getCursorAndConnection()

    query = f"""DELETE FROM {DB.tutors} WHERE 
              username = '{tutor_name}' and
              '{tutor_name}' NOT IN (SELECT tutor_name FROM {DB.course_tutor}) """


    c.execute(query)

    conn.commit()
    conn.close()


def removeTutorsWithNoCourse():
    c, conn = Repo.getCursorAndConnection()

    query = f"""DELETE FROM {DB.tutors} WHERE 
                NOT EXISTS (SELECT * FROM {DB.course_tutor}
                            WHERE tutor_name = username) """

    c.execute(query)

    conn.commit()
    conn.close()

def encrypt_password(password: str):
    """
    Takes a string, applies salting and hashing
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(user, password: str):
    """
    Given a user and a raw password, checks if password is correct
    """
    hashed_password = user[UserModel.password]
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)