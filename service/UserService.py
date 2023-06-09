from flask import render_template, session
import repository.UserRepository as UR
from constants import UserModel, Password


def initializeUserTable():
    return UR.initializeUserTable

def createUser(username: str, password: str, role: str):
    UR.createUser(username, password, role)

def getUserByUsername(username: str):
    return UR.getUserByUsername(username)

def userExistsByUsername(username: str):
    return UR.userExistsByUsername(username)

def login(username: str, password: str):
        user_exists = UR.userExistsByUsername(username)

        if not user_exists:
            error_message = f"There is no user with this username."
            return render_template("opening_screen.html", error_message=error_message)

        user = UR.getUserByUsername(username)
        is_password_correct = UR.check_password(user, password)

        if is_password_correct:
            # Redirect to dashboard if user already exists
            role = user[UserModel.role]
            session["username"] = username
            session["role"] = role

            return render_template("dashboard.html", username=username, role=role)

        else:
            error_message = f"Incorrect password."
            return render_template("opening_screen.html", error_message=error_message)
        
def signup(username: str, password: str, role: str):
    is_valid, error_template = validate_credentials(username, password)

    if not is_valid:
        return error_template

    UR.createUser(username, password, role)

    session["username"] = username
    session["role"] = role

    return render_template("dashboard.html", username=username, role=role)

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
