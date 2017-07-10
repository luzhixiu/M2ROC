from flask import Flask, redirect, url_for, request

app=Flask(__name__)


@app.route('/success/<name>')
def success(name):
	return '%s'% name




@app.route('/login',methods = ['POST', 'GET'])
def  login():
	if request.method == 'POST':
		fname=request.form['firstname']
		lname=request.form['lastname']
		fname=fname+" "+lname
		print(fname)	
		return redirect(url_for('success',name=fname))




if __name__ == '__main__':
   app.run(debug = True)

