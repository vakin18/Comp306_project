class DB:
    users = "users_db"
    project_db = "project_db.db"
    courses = "courses_db"
    cubicle = "cubicles_db"

class UserModel:
    username = 0
    password = 1
    role = 2

class CourseModel:
    code = 0
    name = 1

class Password:
    MIN_LENGTH = 3

class Tutor:
    MAX_PERIODS = 3

USER_TUPLES = [('buzun', '12345', 'admin'),
               ('basar', '12345', 'student'),
               ('vedat', '12345', 'student'),
               ('arda', '12345', 'student')]

STUDENT_TUPLES = [(f"student{i}", "password", "student") for i in range(20)]


COURSE_TUPLES = [('comp306', 'database management systems', 'buzun'),
                 ('comp301', 'programming language concepts', 'basar'),
                 ('comp304', 'operating systems', 'vedat'),
                 ('comp302', 'something something', None),
                 ('comp201', 'computer systems & programming', None),
                 ('comp202', 'data structures & algorithms', None),
                 ('comp106', 'discrete math', None),
                 ('comp100', 'intro to computer sciences', None),
                 ('comp305', 'algorithms and complexitiy', None),
                 ('turk100', 'turkish speech & composition', None),
                 ('acwr101', 'academic writing', None)]