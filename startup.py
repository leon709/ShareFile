# -*- coding:utf-8 -*-

import sys
import os
from werkzeug.utils import secure_filename
import flask
from flask import (Flask,
                   request,
                   render_template,
                   make_response,
                   send_file,
                   redirect)
from mylogger import mylogger
import settings
import util

app = Flask(__name__)

log = mylogger.get_instance()


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    rs = {'name': name}
    return render_template('hello.html', rs=rs)


@app.route('/', methods=['POST', 'GET'])
@app.route('/filelist', methods=['POST', 'GET'])
def filelist():
    todir = request.form.get("todir", "")
    current_dir = request.form.get("current_dir", "")
    if not current_dir:
        current_dir = settings.HOME_PATH

    next_dir = current_dir
    if todir:
        if todir == "..":
            path_split = current_dir.split(os.path.sep)
            if len(path_split) > 1:
                path_split.pop()
            next_dir = os.path.sep.join(path_split)
        else:
            next_dir = os.path.join(current_dir, todir)

    next_dir += os.path.sep
    log.debug("cd %s", next_dir)
    flist = []
    for f in os.listdir(next_dir):
        abs_path = os.path.join(next_dir, f)
        if os.path.isdir(abs_path):
            flist.append((True, f, "-"))
        else:
            fsize = os.path.getsize(abs_path)
            flist.append((False, f, util.getFileSizeString(fsize)))

    current_dir = format_path_spliter(next_dir)
    flist.sort(cmp=None, key=None, reverse=True)
    rs = {'filelist': flist, "todir": "", "current_dir": current_dir}
    return render_template('filelist.html', rs=rs)


def format_path_spliter(s, spliter=os.path.sep):
    """
    Remove the duplicate spliter
    """
    path_begin = spliter if s.startswith(spliter) else ""  # windows or linux path
    return path_begin + spliter.join([p for p in s.split(spliter) if p])


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
    rs = {'user': username}
    return render_template('login.html', rs=rs)


def valid_login(username, pwd):
    print username, pwd
    return username and pwd


@app.route('/download', methods=['POST', 'GET'])
def download():
    # return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    filename = request.form.get("todir", "")
    current_dir = request.form.get("current_dir", "")
    if filename and current_dir:
        file_path = os.path.join(current_dir, filename)
        log.info("Downloading file: %s", file_path)
        response = make_response(send_file(file_path))
        response.headers["Content-Disposition"] = "attachment; filename={};".format(filename.encode("utf-8"))
        return response
        # return flask.send_from_directory(current_dir, filename.encode("utf-8"), as_attachment=True)
    else:
        return redirect("/filelist")


@app.route('/getfile/<filename>', methods=['POST', 'GET'])
def getfile(filename):
    file_path = settings.SHARE_PATH
    file_abs_path = file_path + filename
    log.info("Downloading file: %s", file_abs_path)
    response = make_response(send_file(file_abs_path))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
    return response


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    input_file = request.files.get('file')
    if request.method == 'POST' and input_file:
        target_dir = request.form.get("current_dir", "")
        upload_path = os.path.join(target_dir, secure_filename(input_file.filename))
        input_file.save(upload_path)
        log.info("FILE SAVE: %s", upload_path)
    return filelist()


def load_settings():
    try:
        import settings_local
        log.debug("settings_local detected. %s", settings_local)
        for attr in dir(settings_local):
            if not attr.startswith("__") and not attr.endswith("__"):
                setattr(settings, attr, getattr(settings_local, attr))

        app.config['UPLOAD_FOLDER'] = settings.HOME_PATH
    except ImportError:
        log.warning("settings_local not found.")

if __name__ == '__main__':
    load_settings()
    log.info('start up, debug mode: %s', settings.DEBUG)
    log.info('HOME_PATH: %s', settings.HOME_PATH)

    app.run(debug=settings.DEBUG, host='0.0.0.0', port=5001)
