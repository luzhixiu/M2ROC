from flask import Flask, redirect, url_for, request,send_file
import configparser
from werkzeug import secure_filename
import os
from subprocess import call

app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    return 'welcome! %s' % name
    
@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'download.jpg'
    else:
       filename = 'download.jpg'
    return send_file(filename, mimetype='image/jpg')    

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        f=request.files['file']
        workdir=os.path.join(os.getcwd(), 'Input(LeaveOneOut)',f.filename)
        f.save(workdir)
        classifier = request.form['classifier']
        estimators=request.form['estimators']
        avg=request.form['avg']
        interval=request.form['interval']
        plotrange=request.form['plotrange']
        legendsize=request.form['legendsize']
        plotlinewidth=request.form['plotlinewidth']
        legendtitle=request.form['legendtitle']
        testoutput=classifier+" "+estimators+" "+avg+" "+interval+" "+plotrange+" "+legendsize+" "+plotlinewidth+" "+legendtitle        
        settings = configparser.ConfigParser()
        settings._interpolation = configparser.ExtendedInterpolation()
        settings.read('LeaveOneOutConfig.txt')
        settings.set('SectionOne', 'Classifier', str(classifier))   
        settings.set('SectionOne', 'number of estimators', str(estimators))
        settings.set('SectionOne', 'average the result', str(avg))
        settings.set('SectionOne', 'feature selection interval', str(interval)) 
        settings.set('SectionOne', 'plot feature range', str(plotrange))
        settings.set('SectionOne', 'plot lengend size', str(legendsize)) 
        settings.set('SectionOne', 'plot line width', str(plotlinewidth)) 
        settings.set('SectionOne', 'dataset type name', str(legendtitle))         
        call(["python", "LeaveOneOut.py"])
        
        
        
        
        
        with open('LeaveOneOutConfig.txt', 'wb') as configfile:
            settings.write(configfile)        
        
        return redirect(url_for('get_image'))
        return redirect(url_for('success',name =testoutput ))
if __name__ == '__main__':
    app.run(debug = True)

