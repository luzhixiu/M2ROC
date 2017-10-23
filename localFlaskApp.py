from flask import Flask, redirect, url_for, request,send_file,render_template,send_from_directory,session,escape,flash
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
from audioop import avg
app = Flask(__name__)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

avg="Yes"

def getTopFeature():
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    userFolder=os.path.join(os.getcwd(),"userFolder",session["username"])
    configFile=os.path.join(userFolder,"config.txt")
    settings.read(configFile)
    topFeature=settings.get('SectionOne','top feature')
    return topFeature






def getRandomString():
    return ''.join(choice(ascii_uppercase) for i in range(12))



@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
#     if 'username' not in session:
#         return redirect(url_for('start'))
    


@app.errorhandler(KeyError)
def handle_invalid_usage(error):
    
    return render_template("sessionOut.html")


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
    print "started"
    randomString=getRandomString()
    if "username" not in session:
        session["username"]=randomString
    if not os.path.exists(os.path.join(os.getcwd(),"userFolder",session["username"])): #create default folder
        os.mkdir(os.path.join(os.getcwd(),"userFolder",session["username"]))
        
    if not os.path.exists(os.path.join(os.getcwd(),"userFolder",session["username"],"config.txt")): #create default config file
        os.system("cp config.txt "+ os.path.join(os.getcwd(),"userFolder",session["username"]))
    
    command="cp rawiris.csv "+ os.path.join(os.getcwd(),"userFolder",session["username"],"raw.csv")
    return render_template('form.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':       
        f=request.files['file']                
        if f.filename=="":
            command="cp rawiris.csv "+ os.path.join(os.getcwd(),"userFolder",session["username"],"raw.csv")
            print command
            os.system(command)
        else: 
            workdir=os.path.join(os.getcwd(),"userFolder",session["username"],"raw.csv")
            f.save(workdir)
        classifier = request.form['classifier']
        estimators=request.form['estimators']
        fold=request.form['fold']
        legendsize=request.form['legendsize']
        plotlinewidth=request.form['plotlinewidth']
        legendtitle=request.form['legendtitle']   
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        userFolder=os.path.join(os.getcwd(),"userFolder",session["username"])
        configFile=os.path.join(userFolder,"config.txt")
        settings.read(configFile)
        settings.set('SectionOne', 'Classifier', str(classifier))   
        settings.set('SectionOne', 'Number of estimators', str(estimators))                
        settings.set('SectionOne', 'fold', str(fold))

        settings.set('SectionOne', 'Plot lengend size', str(legendsize)) 
        settings.set('SectionOne', 'Plot line width', str(plotlinewidth)) 
        settings.set('SectionOne', 'Dataset type name', str(legendtitle))        
        configPath=os.path.join(os.getcwd(),"userFolder",session["username"],"config.txt")
         
        with open(configPath, 'wb') as configfile:
            settings.write(configfile)               
        call(["python", "main.py","userFolder/"+session["username"]])
        print "end of result fuction"        
        return redirect(url_for('get_auc'))
    
# def getFiveRoc():
    



@app.route('/auclistener',methods = ['POST', 'GET'])

@app.route('/auc',methods=['Post','GET'])
def get_auc():
    global avg
#     if 'es'in avg:
#         return render_template('auc.html')
#     else:
#         return reder_template('fiveRoc.html')
    return render_template('auc.html')
    
    
    
    

@app.route('/AUC',methods=['Post','GET'])
def send_AUC():
    
    return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),"AUC.png" )

@app.route('/aucListener',methods=['Post','GET'])
def auclistener():
    if request.method == 'POST':
        maxFeature=request.form['maxrange']
        global avg
        avg=request.form['avg']
        configPath=os.path.join(os.getcwd(),"userFolder",session["username"],"config.txt")
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(configPath)
        settings.set('SectionOne', 'average the result', str(avg)) 
        settings.set('SectionOne','top feature',str(maxFeature) )
         
        with open(configPath, 'wb') as configfile:
            settings.write(configfile)
        call(["python", "main.py","userFolder/"+session["username"]])
        return redirect(url_for("page3"))

@app.route('/page3',methods=['Post','GET'])
def page3():
    return render_template("page3.html")
    

@app.route('/getROC')
def get_ROC():
        topFeature=getTopFeature()
        rocFileName="TOP_%s_Feature.png"%topFeature
        print rocFileName
        return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),rocFileName)
    

@app.route('/gallery')
def get_gallery():
    static_names = os.listdir('./static')
    imgList=[]
    for name in static_names:
        if hasNumbers(name):
            imgList.append(name)
    
    return render_template("gallery.html", image_names=sorted(imgList,cmp=sortByNumber))



@app.route('/get_zip')
def get_zip():
    userFolder="userFolder/"+session["username"]
    command="zip -r "+userFolder+"/result.zip "+userFolder
    os.system(command)
    
    return send_file(userFolder+"/result.zip",mimetype='application/zip')        

@app.route('/venn')
def venn():
    command="python drawVenn.py "+"userFolder/"+session["username"]+" "+getTopFeature()
    os.system(command)
    return render_template("venn.html")
    
@app.route('/get_Venn')
def get_Venn():
    return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),"venn5.png" )





@app.route('/get_Bar')
def get_Bar():
    return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),"bar.png" )






@app.route('/user')
def user():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'




if __name__ == '__main__':
    app.config['DEBUG'] = True    
    app.run(host="0.0.0.0")