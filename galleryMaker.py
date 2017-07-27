import glob
from dominate import document
from dominate.tags import *
import os


path=os.getcwd()+'/OUTPUT_LOU/*.png'
print path
photos = glob.glob(path)

with document(title='Photos') as doc:
    h1('Photos')
    for path in photos:
        div(img(src=path), _class='photo')


with open('templates/gallery.html', 'w') as f:
    f.write(doc.render())
