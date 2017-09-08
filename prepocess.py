import sys

path=sys.argv[1]
f=open(path,"r")
lines=f.readlines()
f.close()
f=open(path,"w")
start=False
for line in lines:
    if start and  not line.isspace():
        print line
        f.write(line)
    
    if "@data" in line:
        start=True
        