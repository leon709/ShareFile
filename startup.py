# -*- coding:utf-8 -*-

import sys
import os
import flask
from flask import Flask, request, render_template, make_response, send_file, redirect
from mylogger import mylogger
app = Flask(__name__)

import util

log = mylogger.get_instance()

home_path = "D:/JavaOpenSource/"
UPLOAD_FOLDER = home_path
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    rs = {'name':name}
    return render_template('hello.html', rs=rs)

@app.route('/', methods=['POST', 'GET'])
@app.route('/filelist', methods=['POST', 'GET'])
def filelist():
    todir = request.form.get("todir", "")
    current_dir = request.form.get("current_dir", "")
    if not current_dir:
        current_dir = home_path
    
    next_dir = current_dir
    if todir:
        if todir == "..":
            path_split = current_dir.split("/")
            if len(path_split) > 1:
                path_split.pop()
            next_dir = "/".join(path_split)
        else:
            next_dir = current_dir+'/'+todir
    
    next_dir += "/"        
    log.debug("cd %s", next_dir)
    flist = []
    for f in os.listdir(next_dir):
        abs_path = next_dir+"/"+f
        if os.path.isdir(abs_path):
            flist.append((True, f, "-"))
        else:
            fsize = os.path.getsize(abs_path)
            flist.append((False, f, util.getSizeInNiceString(fsize)))
    
    current_dir = "/".join([p for p in next_dir.split("/") if p])
    rs = {'filelist':flist, "todir":"", "current_dir":current_dir}
    return render_template('filelist.html', rs=rs)	

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = ''
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', rs=error)

def log_the_user_in(username):
    rs = {'user':username}
    return render_template('login.html', rs=rs)

def valid_login(username, pwd):
    print username, pwd
    return username and pwd


@app.route('/download', methods=['POST', 'GET'])
def download():
    #return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    filename = request.form.get("todir", "")
    current_dir = request.form.get("current_dir", "")
    if filename and current_dir:
        file_path = os.path.join(current_dir, filename)
        log.info("Downloading file: %s", file_path)
        response = make_response(send_file(file_path))
        response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
        return response
    
    else:
        return redirect("/filelist")

if __name__ == '__main__':
    run_debug = True
    print 'start up, debug mode:', run_debug
    app.run(debug=run_debug, host='0.0.0.0')
    