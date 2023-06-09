from datetime import date
import bcrypt

import repository.Repository as Repo
from constants import DB, USER_TUPLES, STUDENT_TUPLES, UserModel

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

    return

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

def isUserTutor(username: str):
    #TODO: implement this 
    return

def userExistsByUsername(username: str):
    """
    Return true if a user exists in corresponding database with this username, false otherwise.
    """
    user = getUserByUsername(username)

    return not (user is None)


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