from flask import Flask, redirect, url_for, request,send_file,render_template,send_from_directory,session,escape
import configparser
from werkzeug import secure_filename
import os
from subprocess import call
import time
from datetime import timedelta
import random
from random import choice
import numpy as np
from string import ascii_uppercase
app = Flask(__name__)


def getRandomString():
    return 'User '+''.join(choice(ascii_uppercase) for i in range(12))



@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    do not allow cache
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def start():
    randomString=getRandomString()
    session["username"]=randomString
    return render_template('form.html')

@app.route('/user')
def user():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'





@app.route('/result',methods = ['POST', 'GET'])
def result():
    os.chdir("/home/ubuntu/LabTool1") 

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.config['DEBUG'] = True    
    app.run(host="0.0.0.0")