#!/usr/bin/env python3
from flask import Flask, Response, request, redirect, url_for, send_from_directory, abort, render_template
from werkzeug import secure_filename
from threading import Thread
import logging
import os
import json
import time
from random import randint

# Import our configuration
from conf import config

# Import Hyozan stuff
from Hyozan import db
from Hyozan.output import print_log, time_to_string

app = Flask(__name__)


# Pre-start functions
print_log('Main', 'Running authorization towards B2')
print_log('Main', 'Checking for data folder')
if not os.path.exists(config['UPLOAD_FOLDER']):
  print_log('Main', 'Data folder not found, creating')
  os.makedirs(config['UPLOAD_FOLDER'])
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def auth(key):
  if config["KEY"] == "":
    return True
  elif config["KEY"] == key:
    return True
  else:
    return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in config["ALLOWED_EXTENSIONS"]


@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if not auth(request.headers.get('X-Hyozan-Auth')):
      abort(403)
    data = dict()
    file = request.files['file']

    # Only continue if a file that's allowed gets submitted.
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      while os.path.exists(os.path.join(config["UPLOAD_FOLDER"], filename)):
        filename = str(randint(1000,8999)) + '-' + secure_filename(filename)

      thread1 = Thread(target = db.add_file, args = (filename,))
      thread1.start()
      print_log('Thread', 'Adding to DB')
      file.save(os.path.join(config['UPLOAD_FOLDER'], filename))
      #db.add_file(filename)
      thread1.join()

      data["file"] = filename
      data["url"] = config["DOMAIN"] + "/" + filename
      print_log('Main', 'New file processed')

      if request.form["source"] == "web":
        return redirect(url_for('get_file', filename=filename), code=302)
      else:
        return json.dumps(data)

  # Return Web UI if we have a GET request
  elif request.method == 'GET':
    return render_template('upload.html', page=config["SITE_DATA"])


@app.route('/<filename>', methods=['GET'])
def get_file(filename):
  print_log('Main', 'Hit "' + filename + '" - ' + time_to_string(time.time()))
  return send_from_directory(config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
  app.run(
    port=config["PORT"],
    host=config["HOST"],
    debug=config["DEBUG"]
  )
