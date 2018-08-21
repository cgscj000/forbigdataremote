#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 09:07:41 2018

@author: van
"""

import os
import re
from flask import Flask, request, send_from_directory
from werkzeug import secure_filename

#The path to store the uploaded file.
UPLOAD_FOLDER='./'

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def file_accepted(filename):
	"""
	To deciede whether the file form is correct
	"""
	#i=0
	# for '.' in filename:
	#   i+=1
	#I want only one dot appear in the filename
	return '.' in filename and filename.rsplit('.',1)[1] in set(['jpg','JPG','png','PNG','jpeg','JPEG'])

#greeting page:
@app.route('/')
def helloworld():
	return "Greetings. This is a CNN website, go to /upload to upload your images. Only jpg, png and jpeg permitted."

#uploading page
@app.route('/upload', methods=['GET','POST'])
def uploadfile():
	os.system('python communicate_with_cassandra.py ')
	if request.method=='POST':
		file=request.files['file']
		if file and file_accepted(file.filename):
			global filename, number
			filename=secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			a=os.popen('python show.py '+app.config['UPLOAD_FOLDER']+filename)
			number=a.read()
			a.close()
			pred=re.findall(r"\d+\.?\d*",number)
			#print(pred)
			os.system('python communicate_with_cassandra.py '+filename+' '+pred[0])
			return number
		else :
			return '<p> Uploading file refused. Check the form of the file. </p>'
	return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>upload a new file</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit valve=Upload>
    </form>
    '''
#show the file uploaded    
@app.route('/upload/<filename>')
def show_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__=="__main__":
	app.debug=True
	app.run(host='0.0.0.0', port=80)
    
            
            
