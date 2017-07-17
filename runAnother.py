import os
from subprocess import call

validationMethod="LOU"
workdir=str(os.getcwd())+"/PipeLine"
os.chdir(workdir)
filedir=workdir
if(validationMethod=="CV"):
	filedir+="/CrossValidation.py"
else:	
    filedir+="/LeaveOneOut.py"
call(["python", filedir])

