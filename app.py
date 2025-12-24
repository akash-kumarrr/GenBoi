from flask import *
from server import *
from chatbot import *
from dotenv import load_dotenv
import os 

load_dotenv()


key = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect(url_for('signin'))


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':    
        email = request.form.get('email')
        name = get_name(email)
        password = request.form.get('password')
        print(email, password)
        if isCorrectCredentials(email, password):
            session['active_email'] = email
            session['active_name'] = name
            session['active_password'] = password
            print(session['active_name'])
            return redirect(url_for('terminal'))
        else:
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        key = request.form.get('key')
        if not isEmailExists(email):
            push(email, name, password)
            session['active_email'] = email
            session['active_name'] = name
            session['active_password'] = password
            return redirect(url_for('terminal'))
        else:
            return render_template('signup.html', message="EMAIL_EXISTS")

    return render_template('signup.html')


@app.route('/about', methods=['POST', 'GET'])
def about():
    print
    return render_template('about.html')

@app.route('/terminal', methods=['POST', 'GET'])
def terminal():# Default state
    if request.method == 'POST':
        data = request.get_json()
        prompt = data.get('prompt')
        if prompt:
            response = gemini_response(prompt)
            return jsonify({'response': response})
        return jsonify({'response': 'Error: No prompt provided'})

    return render_template('terminal.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template('profile.html', email=session['active_email'], name=session['active_name'])

@app.route('/profile/edit_profile', methods=['POST', 'GET'])
def edit_profile():
    return render_template('edit_profile.html', name=session['active_name'], email=session['active_email'],  password=session['active_password'])

@app.route('/profile/edit_profile/save_changes', methods=['POST', 'GET'])
def save_changes():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        print(email, name, password)
        update_data(session['active_email'], email, name, password)
        session['active_email'] = email
        session['active_name'] = name
        session['active_password'] = password
    return redirect(url_for('profile', name=session.get('active_name')))

if __name__ == '__main__':
    app.run(debug=True)