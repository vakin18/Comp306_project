from flask import Flask, request, render_template, session
import setup
import socket
import service.UserService as US
import service.TutorPeriodService as TPS
import service.PeriodService as PS


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
    return US.login(username, password)


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


@app.route('/addTutor', methods=['POST'])
def addTutor():
    username = request.form.get('username')
    US.createTutor(username)
    periods = PS.getAllPeriods()
    period_strings = PS.periodToString(periods)
    return render_template('dashboard.html', username=session.get("username"), role='admin', periods=period_strings)


@app.route('/addTutorPeriod', methods=['POST'])
def addTutorPeriod():
    tutor_username = request.form.get('username')
    period_strings = request.form.getlist('day_selection')
  
    if DEBUG:
        print(f'period_strings: {period_strings}')

    periods = PS.stringToPeriod(period_strings)

    for day, interval in periods:
        TPS.createTutorPeriod(tutor_username, day, interval)

    periods = PS.getAllPeriods()
    period_strings = PS.periodToString(periods)
    return render_template('dashboard.html', username=session.get("username"), role='admin', periods=period_strings)



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
