from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    return 'welcome! %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        classifier = request.form['classifier']
        file=request.form['file']
        print("classifier")
	print("file")
	output=" "+"File Submited: "+"   "+file+"    "+"Classifier: "+classifier+"   "
        return redirect(url_for('success',name =output ))

if __name__ == '__main__':
    app.run(debug = True)

