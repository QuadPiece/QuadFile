#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, send_from_directory, abort, render_template
from werkzeug import secure_filename
from threading import Thread, Timer
import logging
import os
import random
import json
import time
from random import randint

# Import our configuration
from conf import config

# Import QuadFile stuff
from QuadFile import db
from QuadFile.output import print_log, time_to_string

app = Flask(__name__)


# TODO: Try to turn these into functions or something I dunno
print_log('Main', 'Running in "' + os.getcwd() + '"')
print_log('Main', 'Checking for data folder')
if not os.path.exists(config['UPLOAD_FOLDER']):
  print_log('Main', 'Data folder not found, creating')
  os.makedirs(config['UPLOAD_FOLDER'])
if config["EXTENDED_DEBUG"] == False:
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)


def cleaner_thread():
  # Call itself again after the interval
  cleaner = Timer(config["CLEAN_INTERVAL"], cleaner_thread)
  cleaner.daemon = True # Daemons will attempt to exit cleanly along with the main process, which we want
  cleaner.start()

  # Actual function
  delete_old()


def delete_old():
  print_log('Notice', 'Cleaner running')
  targetTime = time.time() - config["TIME"]
  old = db.get_old_files(targetTime)
  for file in old:
    print_log('Notice', 'Removing old file "' + file["file"] + '"')
    try:
      os.remove(os.path.join(config["UPLOAD_FOLDER"], file["file"]))
    except Exception:
      print_log('Warning', 'Failed to delete old file "' + file["file"] + '"')
    db.delete_entry(file["file"])


def auth(key):
  if config["KEY"] == "":
    return True
  elif config["KEY"] == key:
    return True
  else:
    return False


def error_page(error, code):
  return render_template('error.html', page=config["SITE_DATA"], error=error, code=code)


def allowed_file(filename):
  if config["ALLOW_ALL_FILES"]:
    return True
  else:
    return '.' in filename and filename.rsplit('.', 1)[1] in config["ALLOWED_EXTENSIONS"]


@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    print_log('Web', 'New file received')
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
      thread1.join()

      data["file"] = filename
      data["url"] = config["DOMAIN"] + "/" + filename
      print_log('Main', 'New file processed "' + filename + '"')

      try:
        if request.form["source"] == "web":
          return render_template('link.html', data=data, page=config["SITE_DATA"])
      except Exception:
        return json.dumps(data)
    else:
      print_log('Notice', 'Forbidden file received')
      return error_page(error="This file isn't allowed, sorry!", code=403)

  # Return Web UI if we have a GET request
  elif request.method == 'GET':
    return render_template('upload.html', page=config["SITE_DATA"])

# Def all the static pages
@app.route('/about')
def about():
  return render_template('about.html', page=config["SITE_DATA"])
@app.route('/terms')
def terms():
  return render_template('terms.html', page=config["SITE_DATA"])
@app.route('/privacy')
def privacy():
  return render_template('privacy.html', page=config["SITE_DATA"])
@app.route('/faq')
def faq():
  return render_template('faq.html', page=config["SITE_DATA"])
@app.route('/dmca')
def dmca():
  video = random.choice(os.listdir("static/dmca/"))
  return render_template('dmca.html', page=config["SITE_DATA"], video=video)

# Static resources that browsers spam for
@app.route('/favicon.ico')
def favicon():
  return send_from_directory('static', 'favicon.ico')
@app.route('/apple-touch-icon.png')
def appleTouch():
  return send_from_directory('static', 'logo/152px.png')
@app.route('/robots.txt')
def robotsTxt():
  return send_from_directory('static', 'robots.txt')

# Custom 404
@app.errorhandler(404)
def page_not_found(e):
    return error_page(error="We couldn't find that. Are you sure you know what you're looking for?", code=404), 404
@app.errorhandler(500)
def internal_error(e):
    return error_page(error="Oops, this is an unknown error, not good.", code=500), 500
@app.errorhandler(403)
def no_permission(e):
    return error_page(error="Check your privilege yo", code=403), 403


@app.route('/<filename>', methods=['GET'])
def get_file(filename):
  print_log('Web', 'Hit "' + filename + '" - ' + time_to_string(time.time()))
  try:
    db.update_file(filename)
  except Exception:
    print_log('Warning', 'Unable to update access time. Is the file in the database?')
  return send_from_directory(config['UPLOAD_FOLDER'], filename)

@app.route('/share/<filename>')
@app.route('/file/<filename>')
def serve_legacy(filename):
  return send_from_directory('legacy', filename)


# Configure nginx to use these urls as custom error pages
@app.route('/error/<int:error>')
def nginx_error(error):
  if error == 413:
    return error_page(error="O-o-onii-chan, noo it's too big ~~", code=413), 413
  else:
    return error_page(error="We literally have no idea what just happened", code="Unknown")


if config["DELETE_FILES"]:
  cleaner_thread()
  
if __name__ == '__main__':
  app.run(
    port=config["PORT"],
    host=config["HOST"],
    debug=config["DEBUG"]
  )
