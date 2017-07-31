from flask import Flask, redirect, url_for, request,send_file,render_template
import configparser
from werkzeug import secure_filename
import os
from subprocess import call
import time
app = Flask(__name__)

@app.route('/')
def start():
     return render_template('form.html')
    
@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'download.jpg'
    else:
       filename = 'download.jpg'
    return send_file(filename, mimetype='image/jpg')    


@app.route('/auc')
def get_auc():
    return render_template('auc.html')


@app.route('/roc')
def get_roc():
   return render_template('roc.html')



@app.route('/get_zip')
def get_zip():
    os.system("zip -r OUTPUT_LOU.zip OUTPUT_LOU/")
    return send_file("OUTPUT_LOU.zip",mimetype='application/zip')	



def clear():
    os.system("sudo ./reinitiate.sh")
    time.sleep(1)



@app.route('/result',methods = ['POST', 'GET'])
def result():
    clear()
    if request.method == 'POST':   	
        f=request.files['file']                
	if f.filename=="":
            os.system("cp Relief.csv Input\(LeaveOneOut\)/")
        else: 
            workdir=os.path.join(os.getcwd(), 'Input(LeaveOneOut)',f.filename)
   	    f.save(workdir)
        classifier = request.form['classifier']
        estimators=request.form['estimators']
        avg=request.form['avg']
        interval="10"
        plotrange=request.form['plotrange']
        legendsize=request.form['legendsize']
        plotlinewidth=request.form['plotlinewidth']
        legendtitle=request.form['legendtitle']
        #testoutput=classifier+" "+estimators+" "+avg+" "+interval+" "+plotrange+" "+legendsize+" "+plotlinewidth+" "+legendtitle        
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
        with open('LeaveOneOutConfig.txt', 'wb') as configfile:
            settings.write(configfile)               
	call(["python2", "LeaveOneOut.py"])
        return redirect(url_for('get_auc'))
        
@app.route('/aucListener',methods = ['POST', 'GET'])
def aucListener():
    if request.method == 'POST':
        interval=request.form['interval']
        print interval;
        return redirect(url_for('get_roc'))    



if __name__ == '__main__':
    app.config['DEBUG'] = True	
    app.run(host='0.0.0.0', port=80,)


