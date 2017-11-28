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


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def getTopFeature():
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    userFolder=os.path.join(os.getcwd(),"userFolder",session["username"])
    configFile=os.path.join(userFolder,"config.txt")
    settings.read(configFile)
    topFeature=settings.get('SectionOne','plot feature range')
    return topFeature

def getRandomString():
    return ''.join(choice(ascii_uppercase) for i in range(12))



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
    print "started"
    randomString=getRandomString()
    if "username" not in session:
        session["username"]=randomString
    if not os.path.exists(os.path.join(os.getcwd(),"userFolder",session["username"])): #create default folder
        os.mkdir(os.path.join(os.getcwd(),"userFolder",session["username"]))
        
    if not os.path.exists(os.path.join(os.getcwd(),"userFolder",session["username"],"config.txt")): #create default config file
        os.system("cp config.txt "+ os.path.join(os.getcwd(),"userFolder",session["username"]))
    
    command="cp rawiris.csv "+ os.path.join(os.getcwd(),"userFolder",session["username"],"raw.csv")
    print command
    response=os.system(command)
    print response
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
        legendsize=request.form['legendsize']
        plotlinewidth=request.form['plotlinewidth']
        legendtitle=request.form['legendtitle']   
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        userFolder=os.path.join(os.getcwd(),"userFolder",session["username"])
        configFile=os.path.join(userFolder,"config.txt")
        print configFile
        settings.read(configFile)
        settings.set('SectionOne', 'Classifier', str(classifier))   
        settings.set('SectionOne', 'Number of estimators', str(estimators))
        settings.set('SectionOne', 'Plot lengend size', str(legendsize)) 
        settings.set('SectionOne', 'Plot line width', str(plotlinewidth)) 
        settings.set('SectionOne', 'Dataset type name', str(legendtitle))        
        configPath=os.path.join(os.getcwd(),"userFolder",session["username"],"config.txt")
         
        with open(configPath, 'wb') as configfile:
            settings.write(configfile)               
        call(["python", "main.py","userFolder/"+session["username"]])
        print "end of result fuction"        
        return redirect(url_for('get_auc'))
    
@app.route('/auclistener',methods = ['POST', 'GET'])

@app.route('/auc',methods=['Post','GET'])
def get_auc():
    return render_template('auc.html')

@app.route('/AUC',methods=['Post','GET'])
def send_AUC():
    return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),"AUC.png" )

@app.route('/aucListener',methods=['Post','GET'])
def auclistener():
    if request.method == 'POST':
        maxFeature=request.form['maxrange']
        avg=request.form['avg']
        configPath=os.path.join(os.getcwd(),"userFolder",session["username"],"config.txt")
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read(configPath)
        settings.set('SectionOne', 'average the result', str(avg)) 
        settings.set('SectionOne','plot feature range',str(maxFeature) )
         
        with open(configPath, 'wb') as configfile:
            settings.write(configfile)
        call(["python", "main.py","userFolder/"+session["username"]])
	if 'Y' in avg:
	    return redirect(url_for("page3A"))
	else:
	    return redirect(url_for("page3B")) 
        

@app.route('/page3A',methods=['Post','GET'])
def page3A():
    return render_template("page3A.html")

@app.route('/page3B',methods=['Post','GET'])
def page3B():
    return render_template("page3B.html")

@app.route('/getRelief')
def get_Relief():
        topFeature=getTopFeature()
        rocFileName="%s TOP_%s_Feature.png"%("Relief",topFeature)
        print rocFileName
        return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),rocFileName)

@app.route('/getGainRatio')
def get_GainRatio():
        topFeature=getTopFeature()
        rocFileName="%s TOP_%s_Feature.png"%("GainRatio",topFeature)
        print rocFileName
        return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),rocFileName)

@app.route('/getInfoGain')
def get_InfoGain():
        topFeature=getTopFeature()
        rocFileName="%s TOP_%s_Feature.png"%("InformationGain",topFeature)
        print rocFileName
        return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),rocFileName)

@app.route('/getSymmeUncertain')
def get_SymmeUncertain():
        topFeature=getTopFeature()
        rocFileName="%s TOP_%s_Feature.png"%("SymmeUncertain",topFeature)
        print rocFileName
        return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),rocFileName)

@app.route('/getMRMR')
def get_MRMR():
        topFeature=getTopFeature()
        rocFileName="%s TOP_%s_Feature.png"%("mRMR",topFeature)
        print rocFileName
        return send_from_directory(os.path.join(os.getcwd(),"userFolder",session["username"]),rocFileName)

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


@app.route('/networkVisual/loadFile',methods=['Post','GET'])
def networkVisualLoadFile():
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    if not os.path.exists(netVisualFolder):
        os.mkdir(netVisualFolder)
    return render_template("networkVisualPage1.html")        


@app.route('/networkVisual/getPower',methods=['Post','GET'])
def getPower():
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    return send_from_directory(netVisualFolder,"tmp.png")



@app.route('/networkVisual/config',methods=['Post','GET'])
def networkVisualConfig():  
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    f=request.files['network']
    if f.filename=="":
        command="cp network.csv "+ os.path.join(netVisualFolder,"network.csv")         
        os.system(command)
    else:
        f.save(os.path.join(netVisualFolder,"network.csv"))
    netVisualSourceDir=os.path.join(os.getcwd(),"networkSrc")
    command="%s/run.sh %s 0"%(netVisualSourceDir,netVisualFolder)
    os.system(command)



    return render_template("networkVisualPage2.html") 

@app.route('/networkVisual/result',methods=['Post','GET'])
def networkVisualResult():
    power=request.form['power']
    cut=request.form['cut']
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    configPath=os.path.join(netVisualFolder,"powercut.txt")
    configString= "yes \n %s \n %s"%(power,cut)
    f=open(configPath,"wb+")
    f.write(configString)
    f.close()
    netVisualSourceDir=os.path.join(os.getcwd(),"networkSrc")
    command="%s/run.sh %s 1"%(netVisualSourceDir,netVisualFolder)
    os.system(command)
    template_dir = os.path.abspath(netVisualFolder)

    return redirect(url_for("sendIndex"))  



@app.route('/networkVisual/index',methods=['Post','GET'])
def sendIndex():
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    return send_from_directory(netVisualFolder,"index.html")


@app.route('/networkVisual/style.css',methods=['POST','GET'])
def getSytleCss():
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    return send_from_directory(netVisualFolder,"style.css")

@app.route('/networkVisual/cytoscape.min.js',methods=['POST','GET'])
def getCytoscapseMinJs():
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    return send_from_directory(netVisualFolder,"cytoscape.min.js")

@app.route('/networkVisual/cy-style.json',methods=['POST','GET'])
def getCySytle():
    netVisualFolder=os.path.join(os.getcwd(),"userFolder",session["username"],"netVisualStatic")
    return send_from_directory(netVisualFolder,"cy-style.json")


   















if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host="0.0.0.0",port=80,threaded=True)
