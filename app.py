from flask import Flask, request, render_template, session, url_for, redirect
import setup
import socket
import service.UserService as US
import service.TutorPeriodService as TPS
import service.PeriodService as PS
import service.TutorService as TS
import service.CourseService as CS
import service.CourseTutorService as CTS
import service.TutorPeriodCubicleService as TPCS
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

@app.route('/remove-course', methods=['POST'])
def removeCourse():
    courses = request.form.getlist('course_selection')

    
    for course in courses:
        error_message = CS.deleteCourse(course)

    TS.removeTutorsWithNoCourse()

    return dashboard(error_message=error_message)


@app.route('/add-period', methods=['POST'])
def addPeriod():
    day = request.form.get('day_selection')
    interval = request.form.get('interval_selection')

    error_message = PS.createPeriod(day, interval)

    return dashboard(error_message=error_message)


@app.route('/remove-period', methods=['POST'])
def removePeriod():
    days_intervals = request.form.getlist('period_selection')

    for day_interval in days_intervals:
        day, interval = PS.stringToPeriod([day_interval])[0]
        error_message = PS.deletePeriodByDayAndInterval(day, interval)

    return dashboard(error_message=error_message)


@app.route('/addTutor', methods=['POST'])
def addTutor():
    username = request.form.get('student_selection')
    courses = request.form.getlist('tutor_course_selection')

    error_message = US.createTutor(username, courses)

    return dashboard(error_message=error_message)



@app.route('/assign-course', methods=['POST'])
def assignCourse():
    username = request.form.get('all_tutors')
    courses = request.form.getlist('course_selection')

    for course in courses:
        error_message = CTS.createCourseTutor(course, username)

    # return redirect(url_for("dashboard"))
    return dashboard(error_message=error_message)


@app.route('/addTutorPeriod', methods=['POST'])
def addTutorPeriod():
    tutor_username = request.form.get('all_tutors')
    period_strings = request.form.getlist('period_selection')


    periods = PS.stringToPeriod(period_strings)

    for day, interval in periods:
        error_message = TPS.createTutorPeriod(tutor_username, day, interval)

    return dashboard(error_message=error_message)



@app.route('/select-tutor', methods=['GET'])
def selectTutor():
    selected_tutor = request.args.get("all_tutors")

    periods = PS.getAllPeriods()
    period_strings = PS.periodToString(periods)
    all_courses = CS.getAllCourses()
    all_tutors = TS.getAllTutors()
    assigned_courses = CTS.getCoursesByTutor(selected_tutor)

    return dashboard(selected_tutor=selected_tutor, assigned_courses=assigned_courses)


@app.route('/unassign-course', methods=['POST'])
def unassignCourse():
    selected_tutor = request.form.get('all_tutors')
    assigned_courses = request.form.getlist('course_selection')

    for assigned_course in assigned_courses:
        error_message = CTS.unassignCourse(selected_tutor, assigned_course)
        

    return dashboard(error_message=error_message)


@app.route('/select-tutor-for-period', methods=['GET'])
def selectTutorForPeriod():
    selected_tutor = request.args.get("all_tutors")

    assigned_periods = TPS.getPeriodsByTutor(selected_tutor)
    
    return dashboard(selected_tutor=selected_tutor, assigned_periods=assigned_periods)


@app.route('/select-cubicle', methods=['GET'])
def selectTutorPeriodCubicle():
    selected_period = request.args.get('assinged_period_selection')
    selected_tutor = request.args.get('all_tutors')

    assigned_periods = TPS.getPeriodsByTutor(selected_tutor)

    selected_period_string = PS.stringToPeriod([selected_period])

    error_message, free_cubicles = TPCS.getFreeCubicles(selected_period_string[0][0], selected_period_string[0][1])

    return dashboard(selected_tutor=selected_tutor, assigned_periods=assigned_periods,
                            selected_assigned_period=selected_period.replace(' ', ''), free_cubicles=free_cubicles, error_message=error_message)

@app.route('/assign-cubicle', methods=['POST'])
def assignTutorPeriodCubicle():
    selected_cubicle = request.form.get('cubicle-selection')
    selected_period = request.form.get('assinged_period_selection')
    selected_tutor = request.form.get('all_tutors')

    selected_period_string = PS.stringToPeriod([selected_period])


    error_message = TPCS.createTutorPeriodCubicle(selected_tutor, selected_period_string[0][0], selected_period_string[0][1], selected_cubicle)

    return dashboard(error_message=error_message)









@app.route('/unassign-period', methods=['POST'])
def unassignPeriod():
    selected_tutor = request.form.get('all_tutors')
    assigned_periods = request.form.getlist('period_selection')

    for assigned_period in assigned_periods:
        TPS.unassignPeriod(selected_tutor, assigned_period)

    return dashboard()


@app.route('/selectCourse', methods=['GET'])
def addTutorCourse():
    selected_course = request.args.get("head_tutor_course_selection")
    tutors = TS.getTutorByCourse(selected_course)

    return dashboard(tutors=tutors, selected_course=selected_course)

@app.route('/assingHeadTutor', methods=['POST'])
def assignHeadTutor():
    selected_course = request.form.get('head_tutor_course_selection')
    head_tutor = request.form.get('tutor_selection')


    CS.updateHeadTutorToCourse(selected_course, head_tutor)
    return dashboard()



@app.route('/selectCourseStudent', methods=['GET'])
def getCourseTutors():
    selected_course = request.args.get("course_selection_stu")
    tutors = TS.getTutorByCourse(selected_course)

    return dashboard(tutors=tutors, selected_course=selected_course)

@app.route('/getPeriodsOfTutorStudent', methods=['POST'])
def getTutorPeriods():
    selected_course = request.form.get("course_selection_stu")
    tutors = TS.getTutorByCourse(selected_course)
    selected_tutor = request.form.get("tutor_selection_stu")

    assigned_periods = TPS.getPeriodsByTutor(selected_tutor)

    return dashboard(selected_tutor=selected_tutor, selected_course=selected_course, tutors=tutors, tutorperiods=assigned_periods)

@app.route('/getCubicle', methods=['POST'])
def getCubicle():
    selected_course = request.form.get("course_selection_stu")
    tutors = TS.getTutorByCourse(selected_course)
    selected_tutor = request.form.get("tutor_selection_stu")
    assigned_periods = TPS.getPeriodsByTutor(selected_tutor)

    selected_period = request.form.get('period_selection_stu')

    period = PS.stringToPeriod([selected_period])



    tutorcubicles = TPCS.getCubicleByTutorPeriod(selected_tutor, period[0][0], period[0][1])
    #PS.getPeriod(day, interval)[PeriodModel.id]
    #period_id = period[PeriodModel.id]

    return dashboard(selected_course=selected_course, selected_tutor=selected_tutor, selected_period=selected_period, tutorperiods=assigned_periods,
                     tutors=tutors, tutorcubicles=tutorcubicles)




@app.route('/dashboard', methods=['GET'])
def dashboard(**kwargs):
    role = session.get("role")

    periods = PS.getAllPeriods()  # id,day,interval
    periods = [period[1:3] for period in periods]  # day, interval
    period_strings = PS.periodToString(periods)
    students = US.getAllStudents()
    courses = CS.getAllCourses()
    tutors = TS.getAllTutors()
    all_days, all_intervals = ALL_DAYS, ALL_INTERVALS

    selected_tutor = session.get("username")
    isTutor = US.isTutorByUsername(selected_tutor)
    assigned_periods = TPS.getPeriodsByTutor(selected_tutor)
    periodsOfTutor = PS.stringToPeriod(assigned_periods)
    assigned_courses = CTS.getCoursesByTutor(selected_tutor)
    cubiclesOfTutor = []
    for period in periodsOfTutor:
        cubicle = TPCS.getCubicleByTutorPeriod(selected_tutor, period[0], period[1])
        cubiclesOfTutor.append((period, cubicle))

    return render_template('dashboard.html', username=session.get("username"), role=role, isTutor=isTutor,assigned_courses=assigned_courses, cubiclesOfTutor=cubiclesOfTutor,
                           periods=period_strings, courses=courses, students=students,
                           all_days=all_days, all_intervals=all_intervals, all_tutors=tutors, **kwargs)



def get_ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    return ip_address

if __name__ == '__main__':
    setup  # noqa
    # Setting the host to the IP address of the device #
    host_address = get_ip_address()
    app.run(host=host_address, debug=True, port=5000)
    app.debug = True
