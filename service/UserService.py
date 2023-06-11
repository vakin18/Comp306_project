from flask import render_template, session
import service.PeriodService as PS
import service.CourseTutorService as CTS
import repository.UserRepository as UR
from constants import UserModel, Password

DEBUG = True

def initializeUserTable():
    return UR.initializeUserTable

def createUser(username: str, password: str, role: str):
    UR.createUser(username, password, role)

def createTutor(username: str, courses):
    user_exists = UR.userExistsByUsername(username)
    error_message = ""
    if not user_exists:
        error_message = "Cannot create tutor because user does not exists."
        
        return error_message
    
    isTutor = UR.isTutorByUsername(username)
    if isTutor:

        error_message = "This is already a tutor."
        
        return error_message
    
    UR.createTutor(username)

    for course in courses:
        CTS.createCourseTutor(course, username)

    return error_message


def getUserByUsername(username: str):
    return UR.getUserByUsername(username)

def getAllStudents():
    student_tuples = UR.getAllStudents()
    student_list = [student[0] for student in student_tuples]
    return student_list

def userExistsByUsername(username: str):
    return UR.userExistsByUsername(username)

def isTutorByUsername(username: str):
    return UR.isTutorByUsername(username)

def login(username: str, password: str):
    success = False
    user_exists = UR.userExistsByUsername(username)

    if not user_exists:
        error_message = f"There is no user with this username."
        return success, error_message

    user = UR.getUserByUsername(username)
    is_password_correct = UR.check_password(user, password)

    if is_password_correct:
        # Redirect to dashboard if user already exists
        role = user[UserModel.role]
        session["username"] = username
        session["role"] = role

        periods = PS.getAllPeriods()
        period_strings = PS.periodToString(periods)
        success = True
        return success, ""

    else:
        error_message = f"Incorrect password."
        return success, error_message
        
def signup(username: str, email: str, password: str, role: str):
    is_valid, error_template = validate_credentials(username, password)

    if not is_valid:
        return error_template

    UR.createUser(username, email, password, role)

    session["username"] = username
    session["role"] = role

    periods = PS.getAllPeriods()
    period_strings = PS.periodToString(periods)
    return render_template("dashboard.html", username=username, role=role, periods=period_strings)

def logout():
    if "username" in session:
        del session["username"]

    if "role" in session:
        del session["role"]
    
    return render_template("opening_screen.html")


def validate_credentials(username: str, password: str):
    if UR.userExistsByUsername(username):
        is_valid = False
        error_message = "This username is already taken."
        return is_valid, render_template("opening_screen.html", error_message=error_message)
    
    if not validate_password(password):
        is_valid = False
        error_message = "Invalid password."
        return is_valid, render_template("opening_screen.html", error_message=error_message)

    is_valid = True
    return is_valid, ""

def validate_password(password: str):
    if len(password) < Password.MIN_LENGTH:
        return False
    
    return True
