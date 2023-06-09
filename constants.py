class DB:
    users = "users_db"
    project_db = "project_db.db"

class UserModel:
    username = 0
    password = 1
    role = 2

USER_TUPLES = [('buzun', '12345', 'admin'),
    ('basar', '12345', 'tutor'),
    ('vedat', '12345', 'tutor'),
    ('arda', '12345', 'tutor')]

class Password:
    MIN_LENGTH = 3