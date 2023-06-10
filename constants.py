class DB:
    users = "users_db"
    tutors = "tutors_db"
    project_db = "project_db.db"
    courses = "courses_db"
    cubicles = "cubicles_db"
    periods = "periods_db"
    tutor_period = "tutor_period_db"
    course_tutor = "course_tutor_db"

class UserModel:
    username = 0
    email = 1
    password = 2
    role = 3

class CourseModel:
    code = 0
    name = 1

class PeriodModel:
    id = 0
    day = 1
    interval = 2

class CubicleModel:
    cubicle_number = 0
    location = 1

class Password:
    MIN_LENGTH = 3

class Tutor:
    MAX_PERIODS = 3

USER_TUPLES = [('buzun', "buzun@ku.edu.tr", '12345', 'admin'),
               ('basar', "basar@ku.edu.tr", '12345', 'student'),
               ('vedat', "vedat@ku.edu.tr", '12345', 'student'),
               ('arda',   "arda@ku.edu.tr", '12345', 'student')]

STUDENT_TUPLES = [(f"student{i}", f"student{i}@ku.edu.tr", "password", "student") for i in range(20)]

TUTOR_TUPLES = [student[UserModel.username] for student in STUDENT_TUPLES[0:10]]


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


DAYS = ['monday','tuesday']
INTERVALS = ['10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00']

ALL_DAYS = ['monday','tuesday','wednesday','thursday','friday']
ALL_INTERVALS = ['08:00-09:00', '09:00-10:00', '10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00']

COURSE_TUTOR_TUPLES = [('comp306', 'student1'),
                       ('comp306', 'student1'),
                       ('comp306', 'student2'),
                       ('comp306', 'student3'),
                       ('comp301', 'student4'),
                       ('comp302', 'student5'),
                       ('turk100', 'student6'),
                       ('turk100', 'student1')]


PERIOD_TUPLES = []
for day in DAYS:
    for interval in INTERVALS:
        PERIOD_TUPLES.append((day, interval))

CUBICLE_TUPLES = []