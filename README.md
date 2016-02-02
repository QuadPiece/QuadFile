# QuadFile Version 2

A temporary (or permanent, depending on configuration) file sharing service written in Flask.

# Features

* Automatically remove files that aren't accessed often enough
* Supports all filetypes
* Prevents duplicate filenames
* Works on all platforms (as long as they can use basic JavaScript)
* Both easy to set up and use
* Threaded for effective use of resources (Unless you're not on SSD, in which case, enjoy your I/O clogs m8)
* Color-coded and real-time console log
* Easy to use with most applications, such as ShareX

# Requirements

Needed: 

* Python 3 (Python 2 might work, dunno, i don't test that, don't care either)
* sqlite3 package for your OS (To create the database)
* Install flask, currently that should be the only requirement and hopefully forever (``pip install -r requirements.txt``)

Recommended:

* nginx, great for proxy_pass
* gunicorn, allows you to use QuadFile with multiple workers

# Using the thing

* Clone the repo somewhere
* Do ``cp conf.py.sample conf.py``
* Edit ``conf.py`` so that the information is correct
* `sqlite3 files.db < schema.sql`
* If possible, make it listen on ``127.0.0.1`` and then use something like nginx as a reverse proxy for security purposes. Using gunicorn and the WSGI entry point is even better if you know how to do that.
* ``chmod +x run.py`` and then ``./run.py``
* ???
* PROFIT (Hopefully)