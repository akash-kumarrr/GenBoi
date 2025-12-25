from flask import redirect, url_for, Flask, render_template, request, session, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

from server import *
from chatbot import *
from datetime import datetime, date
import requests

response = requests.get('https://ipinfo.io/json')
data = response.json()

create_table()

key = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')

@app.context_processor
def inject_icons():
    # Injects these variables into all templates automatically
    return dict(
        favicon=url_for('static', filename='logo.png'),
        about_icon=url_for('static', filename='genboi_icon_aboutpage.png')
    )

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
            return render_template('signin.html', message="INVALID_CREDENTIALS")
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
    return render_template('about.html', location=data.get('city')+' | '+data.get('country'))

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
    app.run()
