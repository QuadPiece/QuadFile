import sqlite3
import time

def connect(target):
  return sqlite3.connect(target)

def add_file(filename):
  db = connect('files.db')
  db.execute('INSERT INTO files (file, time, accessed) VALUES (?, ?, ?)',
               [filename, time.time(), time.time()])
  db.commit()
  db.close()

def update_file(filename):
  db = connect('files.db')
  db.execute('UPDATE files SET accessed = ? WHERE file = ?',
               [time.time(), filename])
  db.commit()
  db.close()

def add_b2(filename, file_id):
  db = connect('files.db')
  db.execute('UPDATE files SET b2 = ? WHERE file = ?',
               [file_id, filename])
  db.commit()
  db.close()

def get_old_files(targetTime):
  db = connect('files.db')
  cur = db.execute('SELECT file FROM files WHERE accessed <= ?', [targetTime,])
  rv = cur.fetchall()
  db.close()
  return [dict(file=row[0]) for row in rv]

def delete_entry(file):
  db = connect('files.db')
  db.execute('DELETE FROM files WHERE file = ?', [file,])
  db.commit()
  db.close()

def check_value(column, value):
  db = connect('files.db')
  cur = db.execute('SELECT EXISTS(SELECT 1 FROM files WHERE ? = ?)', [column, value])
  rv = cur.fetchone()
  db.commit()
  db.close()
  if rv:
    return False
  else:
    return True