from flask import Flask, request, render_template, session, url_for, redirect
import setup
import socket
import service.UserService as US
import service.TutorPeriodService as TPS
import service.PeriodService as PS
import service.TutorService as TS
import service.CourseService as CS
import service.CourseTutorService as CTS
from constants import ALL_DAYS, ALL_INTERVALS

app = Flask(__name__)
app.secret_key = '306'
app.config['SECRET_KEY'] = '306'
DEBUG = True

@app.route('/', methods=['GET'])
def opening_screen():
    return render_template('opening_screen.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    US.login(username, password)
    success, error_message = US.login(username, password)
    if success:
        return redirect(url_for("dashboard"))
    
    return render_template("opening_screen.html", error_message=error_message)


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role_selection')

    return US.signup(username, email, password, role)



@app.route('/logout', methods=['POST'])
def logout():
    return US.logout()


@app.route('/add-course', methods=['POST'])
def addCourse():
    course_code = request.form.get('new_course_code')
    course_name = request.form.get('new_course_name')

    CS.createCourse(course_code, course_name, None)

    return redirect(url_for("dashboard"))



@app.route('/add-period', methods=['POST'])
def addPeriod():
    day = request.form.get('day_selection')
    interval = request.form.get('interval_selection')

    PS.createPeriod(day, interval)

    return redirect(url_for("dashboard"))


@app.route('/addTutor', methods=['POST'])
def addTutor():
    username = request.form.get('student_selection')
    courses = request.form.getlist('tutor_course_selection')

    US.createTutor(username, courses)

    return redirect(url_for("dashboard"))



@app.route('/assign-course', methods=['POST'])
def assignCourse():
    username = request.form.get('tutor')
    courses = request.form.getlist('course_selection')

    for course in courses:
        CTS.createCourseTutor(course, username)

    return redirect(url_for("dashboard"))


@app.route('/addTutorPeriod', methods=['POST'])
def addTutorPeriod():
    tutor_username = request.form.get('tutor')
    period_strings = request.form.getlist('period_selection')
  

    periods = PS.stringToPeriod(period_strings)

    for day, interval in periods:
        TPS.createTutorPeriod(tutor_username, day, interval)

    return redirect(url_for("dashboard"))


@app.route('/selectCourse', methods=['GET'])
def addTutorCourse():
    selected_course = request.args.get("head_tutor_course_selection")

    periods = PS.getAllPeriods()
    period_strings = PS.periodToString(periods)
    courses = CS.getAllCourses()
    tutors = TS.getTutorByCourse(selected_course)
    
    return render_template('dashboard.html', username=session.get("username"), role='admin', periods=period_strings, courses=courses, tutors=tutors, selected_course=selected_course)

@app.route('/assingHeadTutor', methods=['POST'])
def assignHeadTutor():
    selected_course = request.form.get('head_tutor_course_selection')
    head_tutor = request.form.get('tutor_selection')


    CS.updateHeadTutorToCourse(selected_course, head_tutor)
    return dashboard()

@app.route('/dashboard', methods=['GET'])
def dashboard():
    role = session.get("role")

    if role == "admin":
        periods = PS.getAllPeriods()
        period_strings = PS.periodToString(periods)
        students = US.getAllStudents()
        courses = CS.getAllCourses()

        all_days, all_intervals = ALL_DAYS, ALL_INTERVALS

        return render_template('dashboard.html', username=session.get("username"), role=role, 
                               periods=period_strings, courses=courses, students=students, 
                               all_days=all_days, all_intervals=all_intervals)
    

    return render_template('dashboard.html', username=session.get("username"), role=role)


def get_ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    return ip_address

if __name__ == '__main__':
    setup
    # Setting the host to the IP address of the device #
    host_address = get_ip_address()
    app.run(host=host_address, debug=True, port=5000)
    app.debug = True
